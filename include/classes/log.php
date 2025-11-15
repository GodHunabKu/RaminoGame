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

        // Get table from query (for determining which DB to use)
        $table_pattern = '/FROM\s+(\w+)/i';
        preg_match($table_pattern, $query, $matches);
        $table = isset($matches[1]) ? $matches[1] : '';

        // Determine which database connection to use
        $log_tables = getLogTables();
        if (in_array($table, $log_tables)) {
            $conn = $database->getConnectionLog();
        } else {
            $conn = $database->getConnectionAccount();
        }

        // Count total records
        $count_query = preg_replace('/SELECT\s+\*\s+FROM/i', 'SELECT COUNT(*) as total FROM', $query);
        $count_query = preg_replace('/ORDER BY.*$/i', '', $count_query);

        try {
            $stmt = $conn->prepare($count_query);
            $stmt->execute();
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            $this->total_records = $row['total'] ?? 0;
        } catch(PDOException $e) {
            $this->total_records = 0;
        }

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
     * Display data in table format
     */
    public function dataview($query, $columns_or_search = null, $ban_text = null, $unban_text = null, $edit_text = null) {
        global $database, $site_url;

        // Determine which type of dataview this is
        if (is_array($columns_or_search)) {
            // Log view
            $this->dataviewLog($query, $columns_or_search);
        } else {
            // Players view
            $this->dataviewPlayers($query, $columns_or_search, $ban_text, $unban_text, $edit_text);
        }
    }

    /**
     * Display log data
     */
    private function dataviewLog($query, $columns) {
        global $database;

        try {
            $stmt = $database->runQueryLog($query);
            $stmt->execute();

            while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                echo '<tr>';
                foreach ($columns as $column) {
                    echo '<td>' . htmlspecialchars($row[$column] ?? '', ENT_QUOTES, 'UTF-8') . '</td>';
                }
                echo '</tr>';
            }
        } catch(PDOException $e) {
            echo '<tr><td colspan="' . count($columns) . '" class="text-center text-danger">Error loading data</td></tr>';
        }
    }

    /**
     * Display players data
     */
    private function dataviewPlayers($query, $search, $ban_text, $unban_text, $edit_text) {
        global $database, $site_url;

        try {
            $stmt = $database->runQueryAccount($query);
            $stmt->execute();

            while ($account = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $status_class = $account['status'] == 'OK' ? 'success' : 'danger';
                $status_action = $account['status'] == 'OK' ? $ban_text : $unban_text;
                $modal_target = $account['status'] == 'OK' ? 'banModal' : 'unBanModal';

                echo '<tr>';
                echo '<td id="' . (int)$account['id'] . '">' . htmlspecialchars($account['login'], ENT_QUOTES, 'UTF-8') . '</td>';
                echo '<td>' . htmlspecialchars($account['email'], ENT_QUOTES, 'UTF-8') . '</td>';
                echo '<td>' . htmlspecialchars($account['create_time'], ENT_QUOTES, 'UTF-8') . '</td>';
                echo '<td><span class="badge bg-' . $status_class . '">' . htmlspecialchars($account['status'], ENT_QUOTES, 'UTF-8') . '</span></td>';
                echo '<td>';
                echo '<button type="button" class="btn btn-sm btn-' . $status_class . ' open-accountID" data-bs-toggle="modal" data-bs-target="#' . $modal_target . '" data-id="' . (int)$account['id'] . '">' . htmlspecialchars($status_action, ENT_QUOTES, 'UTF-8') . '</button> ';
                echo '<a class="btn btn-sm btn-warning" href="' . htmlspecialchars($site_url, ENT_QUOTES, 'UTF-8') . 'admin/player_edit/' . (int)$account['id'] . '">' . htmlspecialchars($edit_text, ENT_QUOTES, 'UTF-8') . '</a>';
                echo '</td>';
                echo '</tr>';
            }
        } catch(PDOException $e) {
            echo '<tr><td colspan="5" class="text-center text-danger">Error loading data</td></tr>';
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
