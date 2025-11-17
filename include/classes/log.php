<?php
/**
 * Paginate Class
 * Handles pagination for admin tables
 */
class paginate {
    private $page = 1;
    private $total_records = 0;

    /**
     * Initialize pagination with query and records per page
     * @param string $query The SQL query
     * @param int $rp Records per page
     * @return string Modified query with LIMIT
     */
    public function paging($query, $rp) {
        global $database;

        // Get current page
        $this->page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
        if ($this->page < 1) $this->page = 1;

        // Calculate offset
        $offset = ($this->page - 1) * $rp;

        // Add LIMIT to query
        $newquery = $query . " LIMIT " . $offset . ", " . $rp;

        return $newquery;
    }

    /**
     * Display data in table format for PLAYERS page (characters)
     */
    public function dataview($query, $search = null) {
        global $database;

        try {
            $stmt = $database->runQueryPlayer($query);

            // Bind parameters if search is provided
            if($search !== null) {
                if(!filter_var($search, FILTER_VALIDATE_IP) === false) {
                    $stmt->bindParam(':ip', $search, PDO::PARAM_STR);
                } else {
                    $search_param = '%' . $search . '%';
                    $stmt->bindParam(':search', $search_param, PDO::PARAM_STR);
                }
            }

            $stmt->execute();
            $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
            $this->total_records = count($results);

            foreach($results as $player) {
                // Get account info for this player
                $account_id = $player['account_id'];
                $account_stmt = $database->runQueryAccount("SELECT login, status FROM account WHERE id = :id");
                $account_stmt->bindParam(':id', $account_id, PDO::PARAM_INT);
                $account_stmt->execute();
                $account = $account_stmt->fetch(PDO::FETCH_ASSOC);

                $status_class = ($account && $account['status'] == 'OK') ? 'success' : 'danger';
                $status_text = $account ? $account['status'] : 'UNKNOWN';
                $account_login = $account ? $account['login'] : 'N/A';

                echo '<tr>';
                echo '<td>' . htmlspecialchars($account_login, ENT_QUOTES, 'UTF-8') . '</td>';
                echo '<td>' . htmlspecialchars($player['name'], ENT_QUOTES, 'UTF-8') . '</td>';
                echo '<td>' . htmlspecialchars($player['ip'] ?? 'N/A', ENT_QUOTES, 'UTF-8') . '</td>';
                echo '<td><span class="badge bg-' . $status_class . '">' . htmlspecialchars($status_text, ENT_QUOTES, 'UTF-8') . '</span></td>';
                echo '</tr>';
            }
        } catch(PDOException $e) {
            echo '<tr><td colspan="4" class="text-center text-danger">Error: ' . htmlspecialchars($e->getMessage(), ENT_QUOTES, 'UTF-8') . '</td></tr>';
        }
    }

    /**
     * Display pagination links
     */
    public function paginglink($query, $rp, $first_text, $last_text, $site_url, $param = null) {
        $total_pages = ceil($this->total_records / $rp);

        if ($total_pages <= 1) return;

        // Build URL
        $base_url = rtrim($site_url, '/') . '/' . ltrim($_SERVER['REQUEST_URI'], '/');
        $base_url = strtok($base_url, '?');

        if ($param) {
            $base_url .= '/' . urlencode($param);
        }

        echo '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">';

        // First page
        if ($this->page > 1) {
            echo '<li class="page-item"><a class="page-link" href="' . htmlspecialchars($base_url . '?page=1', ENT_QUOTES, 'UTF-8') . '">' . htmlspecialchars($first_text, ENT_QUOTES, 'UTF-8') . '</a></li>';
            echo '<li class="page-item"><a class="page-link" href="' . htmlspecialchars($base_url . '?page=' . ($this->page - 1), ENT_QUOTES, 'UTF-8') . '">‹</a></li>';
        }

        // Page numbers
        $start = max(1, $this->page - 2);
        $end = min($total_pages, $this->page + 2);

        for ($i = $start; $i <= $end; $i++) {
            $active = ($i == $this->page) ? ' active' : '';
            echo '<li class="page-item' . $active . '"><a class="page-link" href="' . htmlspecialchars($base_url . '?page=' . $i, ENT_QUOTES, 'UTF-8') . '">' . $i . '</a></li>';
        }

        // Last page
        if ($this->page < $total_pages) {
            echo '<li class="page-item"><a class="page-link" href="' . htmlspecialchars($base_url . '?page=' . ($this->page + 1), ENT_QUOTES, 'UTF-8') . '">›</a></li>';
            echo '<li class="page-item"><a class="page-link" href="' . htmlspecialchars($base_url . '?page=' . $total_pages, ENT_QUOTES, 'UTF-8') . '">' . htmlspecialchars($last_text, ENT_QUOTES, 'UTF-8') . '</a></li>';
        }

        echo '</ul></nav>';

        // Show total records
        echo '<p class="text-center text-muted small">Total records: ' . number_format($this->total_records) . ' | Page ' . $this->page . ' of ' . $total_pages . '</p>';
    }
}
?>
