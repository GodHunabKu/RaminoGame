<div class="container">
    <!-- Admin Page Header -->
    <div class="card bg-dark mb-4 mt-3">
        <div class="card-body text-center">
            <div class="admin-header-icon mb-3">
                <i class="fas fa-user-shield fa-3x text-primary"></i>
            </div>
            <h2 class="text-white mb-2"><?php print $a_title; ?></h2>
            <p class="text-muted mb-0">
                <i class="fas fa-shield-alt"></i> Pannello di Amministrazione
            </p>
        </div>
    </div>

    <!-- Admin Page Content -->
    <div class="admin-content-wrapper">
        <?php include 'pages/admin/'.$a_page.'.php'; ?>
    </div>
</div>