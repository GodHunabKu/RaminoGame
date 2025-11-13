<div class="ranking-header">
    <h2><i class="fas fa-trophy"></i> <?php print $lang['ranking']; ?></h2>
    <div class="ranking-tabs">
        <a href="#" class="tab-link active">
            <i class="fas fa-user"></i> <?php print $lang['players']; ?>
        </a>
        <a href="<?php print $site_url; ?>ranking/guilds" class="tab-link">
            <i class="fas fa-shield-alt"></i> <?php print $lang['guilds']; ?>
        </a>
    </div>
</div>

<div class="ranking-content">
    <!-- SEARCH BOX -->
    <div class="search-box">
        <form action="" method="POST">
            <div class="search-input-group">
                <div class="search-icon">
                    <i class="fas fa-search"></i>
                </div>
                <input 
                    type="text" 
                    name="search" 
                    class="search-input" 
                    placeholder="<?php print $lang['name']; ?>" 
                    value="<?php if(isset($search)) print htmlentities($search); ?>"
                >
                <button type="submit" class="search-btn">
                    <i class="fas fa-search"></i> <?php print $lang['search']; ?>
                </button>
            </div>
        </form>
    </div>
    
    <!-- RANKING TABLE -->
    <div class="ranking-table-container">
        <table class="ranking-table-full">
            <thead>
                <tr>
                    <th class="rank-col">#</th>
                    <th class="name-col"><?php print $lang['name']; ?></th>
                    <th class="empire-col"><?php print $lang['empire']; ?></th>
                    <th class="level-col"><?php print $lang['level']; ?></th>
                    <th class="exp-col">EXP</th>
                </tr>
            </thead>
            <tbody>
                <?php 
                    $records_per_page=20;
                    
                    if(isset($search)) {
                        $query = "SELECT id, name, account_id, level, exp FROM player WHERE name NOT LIKE '[%]%' AND name LIKE :search ORDER BY level DESC, exp DESC, playtime DESC, name ASC";
                        $newquery = $paginate->paging($query,$records_per_page);
                        $paginate->dataview($newquery, $search);
                    } else {
                        $query = "SELECT id, name, account_id, level, exp FROM player WHERE name NOT LIKE '[%]%' ORDER BY level DESC, exp DESC, playtime DESC, name ASC";
                        $newquery = $paginate->paging($query,$records_per_page);
                        $paginate->dataview($newquery);
                    }
                ?>
            </tbody>
        </table>
    </div>
    
    <!-- PAGINATION -->
    <div class="pagination-wrapper">
        <?php
            if(isset($search))
                $paginate->paginglink($query,$records_per_page,$lang['first-page'],$lang['last-page'],$site_url,$search);
            else
                $paginate->paginglink($query,$records_per_page,$lang['first-page'],$lang['last-page'],$site_url);
        ?>
    </div>
</div>