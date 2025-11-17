<?php
/**
 * ==========================================
 * CLASSIFICA GIOCATORI - ONE SERVER (Modern Layout)
 * ==========================================
 */
?>

<style>
/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Base Variables & Fonts */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

:root {
    --color-primary: #E74C3C; /* Red/Crimson */
    --color-primary-dark: #C0392B;
    --color-text-light: #F5F5F5;
    --color-text-dark: #A0A0A0;
    --color-box-bg: rgba(40, 40, 40, 0.95);
    --transition-smooth: all 0.3s ease;
    --transition-fast: all 0.2s ease-out;
    --font-primary: 'Inter', sans-serif;
    --font-secondary: 'Cinzel', serif;
    --shadow-lg: 0 8px 30px rgba(0, 0, 0, 0.4);
    --shadow-sm: 0 4px 10px rgba(0, 0, 0, 0.2);
}

body {
    font-family: var(--font-primary);
    background: #1E1E1E;
    color: var(--color-text-light);
}

/* Container */
.ranking-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

/* Keyframes */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes heroRotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes iconFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes ripple-effect {
    to {
        transform: translate(-50%, -50%) scale(2);
        opacity: 0;
    }
}

/* ==================== RANKING PAGE STYLES (Modernized) ==================== */
.ranking-page-wrapper {
    width: 100%;
    animation: fadeIn 0.6s ease-out;
}

.ranking-hero-header {
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.15), rgba(192, 57, 43, 0.08));
    backdrop-filter: blur(20px);
    border: 2px solid rgba(231, 76, 60, 0.3);
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 30px;
    box-shadow: var(--shadow-lg);
}

.ranking-hero-content {
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}

.ranking-title-section {
    display: flex;
    align-items: center;
    gap: 20px;
}

.ranking-icon-wrapper {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 30px rgba(231, 76, 60, 0.6);
    animation: iconFloat 3s ease-in-out infinite;
}

.ranking-icon-wrapper i {
    font-size: 40px;
    color: white;
}

.ranking-title-text h1 {
    font-family: var(--font-secondary);
    font-size: 36px;
    color: var(--color-primary);
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 0 2px 20px rgba(231, 76, 60, 0.4);
}

.ranking-title-text p {
    font-size: 16px;
    color: var(--color-text-dark);
    margin: 5px 0 0 0;
}

.ranking-tabs-container {
    display: flex;
    gap: 15px;
    background: rgba(0, 0, 0, 0.3);
    padding: 8px;
    border-radius: 12px;
    border: 1px solid rgba(231, 76, 60, 0.2);
}

.ranking-tab {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 25px;
    background: transparent;
    border: 2px solid transparent;
    border-radius: 8px;
    color: var(--color-text-dark);
    font-weight: 600;
    text-decoration: none;
    transition: var(--transition-smooth);
    position: relative;
    overflow: hidden;
}

.ranking-tab.active {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    color: white;
    border-color: transparent;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
}

/* ==================== SEARCH SECTION ==================== */
.ranking-search-section {
    background: var(--color-box-bg);
    border: 1px solid rgba(231, 76, 60, 0.15);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: var(--shadow-lg);
}

.search-form-wrapper {
    display: flex;
    gap: 15px;
    align-items: center;
}

.search-input-container {
    flex: 1;
    position: relative;
}

.search-icon-left {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-primary);
    font-size: 20px;
    z-index: 1;
    pointer-events: none;
}

.search-input-field {
    width: 100%;
    padding: 18px 20px 18px 55px;
    background: rgba(0, 0, 0, 0.4);
    border: 2px solid rgba(231, 76, 60, 0.2);
    border-radius: 12px;
    color: var(--color-text-light);
    font-size: 16px;
    font-weight: 500;
    transition: var(--transition-smooth);
    outline: none;
}

.search-submit-btn {
    padding: 18px 35px;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
    transition: var(--transition-smooth);
    position: relative;
    overflow: hidden;
}

.search-submit-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 25px rgba(231, 76, 60, 0.5);
}

/* ==================== RANKING TABLE STRUCTURE & STYLES ==================== */
.ranking-table-section {
    background: var(--color-box-bg);
    border: 1px solid rgba(231, 76, 60, 0.15);
    border-radius: 16px;
    padding: 0;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    margin-bottom: 30px;
}

.table-wrapper {
    overflow-x: auto;
}

.ranking-table-modern {
    width: 100%;
    border-collapse: collapse;
    background: transparent;
    table-layout: fixed; /* Importante per width fisse */
}

.ranking-table-modern thead {
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.25) 0%, rgba(192, 57, 43, 0.15) 100%);
    border-bottom: 3px solid var(--color-primary);
}

.ranking-table-modern thead th {
    padding: 20px;
    text-align: left;
    color: var(--color-primary);
    font-weight: 700;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    white-space: nowrap;
}

.ranking-table-modern thead th:first-child {
    text-align: center;
}

.ranking-table-modern tbody tr {
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    transition: var(--transition-fast);
    position: relative;
}

.ranking-table-modern tbody tr:hover {
    background: rgba(231, 76, 60, 0.08);
}

.ranking-table-modern tbody tr:nth-child(odd) {
    background: rgba(0, 0, 0, 0.2);
}

.ranking-table-modern tbody td {
    padding: 18px 20px;
    color: var(--color-text-dark);
    font-size: 15px;
    font-weight: 500;
    vertical-align: middle;
}

/* --- COLUMN WIDTHS & ALIGNMENT --- */

.rank-column {
    width: 80px; 
    text-align: center;
}

.name-column {
    font-weight: 700;
    color: var(--color-text-light);
    font-size: 17px;
    width: 35%; 
    min-width: 150px;
}

.empire-column {
    width: 120px; 
    text-align: center;
}

.level-column {
    font-weight: 700;
    color: var(--color-primary);
    font-size: 18px;
    width: 120px; 
    text-align: center;
}

.exp-column {
    font-family: 'Courier New', monospace;
    color: var(--color-text-light);
    font-weight: 700;
    font-size: 17px;
    text-align: right;
    width: auto; 
    min-width: 150px;
}

/* --- RANK BADGES & MEDALS --- */

.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(231, 76, 60, 0.3) 0%, rgba(192, 57, 43, 0.2) 100%);
    color: var(--color-primary);
    font-weight: 700;
    font-size: 18px;
    border: 2px solid rgba(231, 76, 60, 0.3);
    transition: var(--transition-smooth);
}

.rank-column img.rank-medal {
    width: 65px; 
    height: auto;
    vertical-align: middle;
    transition: transform 0.3s ease;
    filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.7));
}

.ranking-table-modern tbody tr:hover .rank-column img.rank-medal {
    transform: scale(1.15);
}

/* Empire Icons */
.empire-icon {
    width: 30px;
    height: 30px;
    display: inline-block;
    vertical-align: middle;
    transition: var(--transition-smooth);
}

/* ==================== PAGINATION STYLES (Corretto z-index) ==================== */
.pagination-section {
    display: flex;
    justify-content: center;
    padding: 30px 0;
    position: relative; /* Fix Overlay */
    z-index: 5; /* Fix Overlay */
}

.pagination-modern {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.pagination-modern a,
.pagination-modern span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 50px;
    height: 50px;
    padding: 0 18px;
    background: var(--color-box-bg);
    border: 2px solid rgba(231, 76, 60, 0.2);
    border-radius: 10px;
    color: var(--color-text-dark);
    font-weight: 700;
    font-size: 15px;
    text-decoration: none;
    transition: var(--transition-smooth);
    box-shadow: var(--shadow-sm);
    
    /* FIX CRITICO PER CLICK */
    position: relative; 
    z-index: 10;       
    cursor: pointer; 
}

.pagination-modern a:hover {
    background: rgba(231, 76, 60, 0.2);
    border-color: var(--color-primary);
    color: var(--color-text-light);
    transform: translateY(-3px);
}

.pagination-modern .active,
.pagination-modern span {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border-color: transparent;
    color: white;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
    cursor: default;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 1024px) {
    .ranking-hero-content { flex-direction: column; align-items: flex-start; }
    .ranking-tabs-container { width: 100%; }
    .ranking-tab { flex: 1; justify-content: center; }
}

@media (max-width: 768px) {
    .search-form-wrapper { flex-direction: column; }
    .search-submit-btn { width: 100%; justify-content: center; }
    .ranking-table-modern thead th, .ranking-table-modern tbody td { padding: 15px 10px; font-size: 14px; }
    .exp-column { display: none; } 
    .level-column { width: 80px; }
    .empire-column { width: 80px; }
}

@media (max-width: 480px) {
    .empire-column { display: none; } 
    .level-column { width: 60px; }
}
</style>

<div class="ranking-container">
    <div class="ranking-page-wrapper">
        
        <!-- HERO HEADER -->
        <div class="ranking-hero-header">
            <div class="ranking-hero-content">
                <div class="ranking-title-section">
                    <div class="ranking-icon-wrapper">
                        <i class="fas fa-trophy"></i>
                    </div>
                    <div class="ranking-title-text">
                        <h1>CLASSIFICA</h1>
                        <p>Scopri i migliori giocatori del server</p>
                    </div>
                </div>
                
                <div class="ranking-tabs-container">
                    <a href="<?php print $site_url; ?>ranking/players" class="ranking-tab active">
                        <i class="fas fa-user"></i>
                        <span>Giocatori</span>
                    </a>
                    <a href="<?php print $site_url; ?>ranking/guilds" class="ranking-tab">
                        <i class="fas fa-shield-alt"></i>
                        <span>Gilde</span>
                    </a>
                </div>
            </div>
        </div>
        
        <!-- SEARCH SECTION -->
        <div class="ranking-search-section">
            <form action="" method="POST" class="search-form-wrapper">
                <div class="search-input-container">
                    <div class="search-icon-left">
                        <i class="fas fa-search"></i>
                    </div>
                    <input 
                        type="text" 
                        name="search" 
                        class="search-input-field" 
                        placeholder="Nome" 
                        value="<?php if(isset($search)) print htmlspecialchars($search, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>
                <button type="submit" class="search-submit-btn">
                    <i class="fas fa-search"></i>
                    <span>Cerca</span>
                </button>
            </form>
        </div>
        
        <!-- RANKING TABLE -->
        <div class="ranking-table-section">
            <div class="table-wrapper">
                <table class="ranking-table-modern">
                    <thead>
                        <tr>
                            <th class="rank-column">#</th>
                            <th class="name-column">NOME</th>
                            <th class="empire-column">REGGNO</th>
                            <th class="level-column">LIVELLO</th>
                            <th class="exp-column">EXP</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php 
                            $records_per_page = 20;
                            
                            if(isset($search)) {
                                $query = "SELECT id, name, account_id, level, exp FROM player WHERE name NOT LIKE '[%]%' AND name LIKE :search ORDER BY level DESC, exp DESC, playtime DESC, name ASC";
                                $newquery = $paginate->paging($query, $records_per_page);
                                $paginate->dataview($newquery, $search);
                            } else {
                                $query = "SELECT id, name, account_id, level, exp FROM player WHERE name NOT LIKE '[%]%' ORDER BY level DESC, exp DESC, playtime DESC, name ASC";
                                $newquery = $paginate->paging($query, $records_per_page);
                                $paginate->dataview($newquery);
                            }
                        ?>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- PAGINATION CORRETTA -->
        <div class="pagination-section">
            <div class="pagination-modern">
                <?php
                    if(isset($search))
                        $paginate->paginglink($query, $records_per_page, $lang['first-page'], $lang['last-page'], $site_url, $search, 'players');
                    else
                        $paginate->paginglink($query, $records_per_page, $lang['first-page'], $lang['last-page'], $site_url, NULL, 'players');
                ?>
            </div>
        </div>
        
    </div>
</div>

<script>
// ==================== RANKING PLAYERS PAGE JAVASCRIPT ====================
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scroll animation for table rows
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)'; 
                }, index * 50);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const tableRows = document.querySelectorAll('.ranking-table-modern tbody tr');
    tableRows.forEach(row => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(20px)';
        row.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(row);
    });
    
    // Enhanced hover effect for rank badges
    const rankBadges = document.querySelectorAll('.rank-badge');
    rankBadges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.15) rotate(5deg)';
            this.style.boxShadow = '0 0 20px rgba(231, 76, 60, 0.5)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // Add ripple effect to search button
    const searchBtn = document.querySelector('.search-submit-btn');
    if (searchBtn) {
        searchBtn.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
                animation: ripple-effect 0.6s ease-out;
            `;
            
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    }
    
    // Console art
    console.log('%c?? RANKING PLAYERS', 'color: #E74C3C; font-size: 20px; font-weight: bold;');
    console.log('%c? Pagina caricata con successo!', 'color: #27AE60; font-size: 14px;');
});
</script>