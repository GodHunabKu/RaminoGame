<?php
class paginate
{
	private $db;
	
	public function __construct()
	{
		global $host, $user, $password;
		// Assumiamo che Database sia definito altrove
		$database = new Database(); 
		$db = $database->dbConnection($host, "player", $user, $password);
		$this->db = $db;
    }
	
    /**
     * Metodo dataview per la Classifica Gilde
     */
	public function dataview($query, $search=NULL)
	{
		global $site_url;
		
		$stmt = $this->db->prepare($query);
		if($search)
			$stmt->bindValue(':search', $search.'%');
		$stmt->execute();
		
		// 1. Calcola il rank iniziale in base alla paginazione
		$number = 0;
		$records_per_page = 20; 
		if(isset($_GET["page_no"]))
		{
			if(is_numeric($_GET["page_no"]))
			{
				if($_GET["page_no"]>1)
					$number = ($_GET["page_no"]-1)*$records_per_page;
			}
		}

		if($stmt->rowCount() > 0)
		{
			while($row=$stmt->fetch(PDO::FETCH_ASSOC))
			{	
				$number++;
				$leader_name = getPlayerName($row['master']);
				$empire_id = get_player_empire(getAccountID($row['master'])); 
				$empire_name = empire_name($empire_id); 

				
				// --- LOGICA PER RANK (IMMAGINI TOP 3) ---
				$rank_content = '<span class="rank-badge">' . $number . '</span>';
				
				if ($number == 1) {
					$rank_content = '<img src="' . $site_url . 'images/top1.png" alt="Rank 1" class="rank-medal">';
				} elseif ($number == 2) {
					$rank_content = '<img src="' . $site_url . 'images/top2.png" alt="Rank 2" class="rank-medal">';
				} elseif ($number == 3) {
					$rank_content = '<img src="' . $site_url . 'images/top3.png" alt="Rank 3" class="rank-medal">';
				}
				// ------------------------------------------

				?>
			<tr>
				<td class="rank-column"><?php print $rank_content; ?></td>
				<td class="guild-name-column"><div class="guild-icon"><i class="fas fa-users"></i></div><?php print htmlspecialchars($row['name'], ENT_QUOTES, 'UTF-8'); ?></td>
				<td class="leader-column"><div class="leader-icon"><i class="fas fa-user-alt"></i></div><?php print htmlspecialchars($leader_name, ENT_QUOTES, 'UTF-8'); ?></td>
				<td class="empire-column"><img src="<?php print $site_url; ?>images/empire/<?php print $empire_id; ?>.png" alt="<?php print $empire_name; ?>" class="empire-icon"></td>
				<td class="level-column"><?php print $row['level']; ?></td>
				<td class="points-column"><?php print number_format($row['ladder_point'], 0, '', '.'); ?></td>
			</tr>
				<?php
			}
		}
		else
		{
			?>
			<tr>
			<td colspan="6" style="text-align: center; padding: 50px; color: var(--color-text-dark);">
				<i class="fas fa-search" style="font-size: 48px; opacity: 0.3; display: block; margin-bottom: 15px;"></i>
				Nessuna gilda trovata
			</td>
			</tr>
			<?php
		}
		
	}
	
	public function paging($query,$records_per_page)
	{
		$starting_position=0;
		if(isset($_GET["page_no"]))
		{
			if(is_numeric($_GET["page_no"]))
				if($_GET["page_no"]>1)
					$starting_position=($_GET["page_no"]-1)*$records_per_page;
		}
		$query2=$query." limit $starting_position,$records_per_page";
		return $query2;
	}
	
	public function paginglink($query,$records_per_page,$first,$last,$self,$search=NULL, $type='guilds')
	{		
		$self = $self.'ranking/'.$type.'/';
		
		$sql = "SELECT count(*) ".strstr($query, 'FROM');
		
		$stmt = $this->db->prepare($sql);
		if($search)
			$stmt->bindValue(':search', $search.'%');
		$stmt->execute(); 
		
		$total_no_of_records = $stmt->fetchColumn();
		
		if($total_no_of_records > 0)
		{
			$total_no_of_pages=ceil($total_no_of_records/$records_per_page);
			$current_page=1;
			if(isset($_GET["page_no"]) && is_numeric($_GET["page_no"]))
			{
				$current_page=$_GET["page_no"];
				
				// Reindirizzamento per pagina fuori limite
				if($current_page < 1) {
					print "<script>top.location='".$self."1'</script>";
					return;
				}
				if($current_page > $total_no_of_pages) {
					print "<script>top.location='".$self.$total_no_of_pages."'</script>";
					return;
				}
			}
			
			// Previous
			if($current_page!=1)
			{
				$previous = $current_page-1;
				if($search)
					print "<a href='".$self.$previous."/".$search."'><i class='fas fa-chevron-left'></i></a>";
				else
					print "<a href='".$self.$previous."'><i class='fas fa-chevron-left'></i></a>";
			}
			
			// Pages
            $start_page = $current_page;
			if($current_page+3>$total_no_of_pages) {
                $start_page = max(1, $total_no_of_pages - 3);
            }
            
			for($i=$start_page;$i<=$start_page+3;$i++)
				if($i==$current_page)
					print '<span class="active">'.$i.'</span>';
				else if($i>$total_no_of_pages)
					break;
				else
				{
					if($search)
						print "<a href='".$self.$i."/".$search."'>".$i."</a>";
					else
						print "<a href='".$self.$i."'>".$i."</a>";
				}
			
			// Next
			if($current_page!=$total_no_of_pages)
			{
				$next=$current_page+1;
				if($search)
					print "<a href='".$self.$next."/".$search."'><i class='fas fa-chevron-right'></i></a>";
				else
					print "<a href='".$self.$next."'><i class='fas fa-chevron-right'></i></a>";
			}
		}
	}
}
?>