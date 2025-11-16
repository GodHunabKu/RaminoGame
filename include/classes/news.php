<?php

class paginate
{
	private $db;
	
	public function __construct()
	{
		$database = new Database();
		$db = $database->dbConnection("", "", "", "", "yes");
		$this->db = $db;
    }
	
	public function add($title,$content,$category)
	{
		try
		{		
			$time = date("Y-m-d H:i:s", time());
			
			$stmt = $this->db->prepare("INSERT INTO news(title, content, time, category) VALUES(:title, :content, :time, :category)");
			$stmt->bindparam(":title", $title);
			$stmt->bindparam(":content", $content);
			$stmt->bindparam(":time", $time);
			$stmt->bindparam(":category", $category);
				
			$stmt->execute();
			
			return $stmt;
		}
		catch(PDOException $e)
		{
			print 'ERROR';
		}
	}
	
	public function edit($id, $title, $content)
	{
		try
		{		
			$time = date("Y-m-d H:i:s", time());
			
			$stmt = $this->db->prepare("UPDATE news SET title=:title, content=:content, time=:time WHERE id=:id");
			$stmt->bindparam(":title", $title);
			$stmt->bindparam(":content", $content);
			$stmt->bindparam(":time", $time);
			$stmt->bindparam(":id", $id);
				
			$stmt->execute();
			
			return $stmt;
		}
		catch(PDOException $e)
		{
			//echo $e->getMessage();
			print 'ERROR';
		}
	}
	
	public function delete_article($id)
	{
		try
		{		
			$stmt = $this->db->prepare("DELETE FROM news WHERE id = :id");
			$stmt->bindparam(":id", $id);
				
			$stmt->execute();
			
			return $stmt;
		}
		catch(PDOException $e)
		{
			//echo $e->getMessage();
			print 'ERROR';
		}
	}
	
	public function check_id($id)
	{
		try
		{		
			$stmt = $this->db->prepare("SELECT id FROM news WHERE id = :id LIMIT 1");
			$stmt->bindparam(":id", $id);
				
			$stmt->execute();
			$result = $stmt->fetchAll();
			
			if(count($result))
				return 1;
			else return 0;
		}
		catch(PDOException $e)
		{
			//echo $e->getMessage();
			print 'ERROR';
		}
	}
	
	public function read($id)
	{
		try
		{		
			$stmt = $this->db->prepare("SELECT * FROM news WHERE id = :id LIMIT 1");
			$stmt->bindparam(":id", $id);
				
			$stmt->execute();
			$result = $stmt->fetch(PDO::FETCH_ASSOC);
			
			return $result;
		}
		catch(PDOException $e)
		{
			//echo $e->getMessage();
			print 'ERROR';
		}
	}
	
	public function dataview($query, $sure, $web_admin, $news_lvl, $site_url, $read_more)
	{
		$stmt = $this->db->prepare($query);
		$stmt->execute();
		$rowCount = count($stmt->fetchAll());
		
		$stmt = $this->db->prepare($query);
		$stmt->execute();
		
		if($rowCount>0)
		{
			while($row=$stmt->fetch(PDO::FETCH_ASSOC))
			{
				$big = false;
				$string = $row['content'];
?>
  <div class="content-xy">
    <div class="xy-title">
      <div class="left">
        <h3><a href="<?php print $site_url.'read/'.$row['id']; ?>"><?php print $row['title']; ?></a>
											<?php if($web_admin>=$news_lvl) { ?><a href="<?php print $site_url.'read/'.$row['id']; ?>"><i class="fas fa-edit" aria-hidden="true"></i></a> <a href="<?php print $site_url.'?delete='.$row['id']; ?>" onclick="return confirm('<?php print $sure; ?>');"><i style="color:red;" class="fas fa-trash fa-2" aria-hidden="true"></i></a><?php } ?></h3>
      </div>
      <div class="right">
        <ul class="xy">
          <li><?php print time_elapsed_string($row['time']); ?></li>
          <li>By Admin</li>
        </ul>
      </div>
    </div>
    <div class="xy-text-cont">
      <p><?php print $string; ?></p>
    </div>
  </div>
                <?php
			}
		}
		else
		{
			?>
            <p style="padding: 10px;">Nothing here...</p>
            <?php
		}
		
	}
	
	public function paging($query,$records_per_page)
	{
		$starting_position=0;
		if(isset($_GET["page_no"]))
		{
			if(is_numeric($_GET["page_no"]))
				$starting_position=($_GET["page_no"]-1)*$records_per_page;
		}
		$query2=$query." limit $starting_position,$records_per_page";
		return $query2;
	}
	
	public function paginglink($query,$records_per_page,$first,$last,$self,$category)
	{		
		$self = $self.'news/'.$category.'/';
		
		$sql = "SELECT count(*) ".strstr($query, 'FROM');
		
		$stmt = $this->db->prepare($sql);
		$stmt->execute(); 
		
		$total_no_of_records = $stmt->fetchColumn();
		
		if($total_no_of_records > 0)
		{
			?><div class="pagination"><div class="buttons"><?php
			$total_no_of_pages=ceil($total_no_of_records/$records_per_page);
			$current_page=1;
			if(isset($_GET["page_no"]))
			{
				if(is_numeric($_GET["page_no"]))
				{
					$current_page=$_GET["page_no"];
					
					if($_GET["page_no"]<1)
						print "<script>top.location='".$self."'</script>";
					else if($_GET["page_no"]>$total_no_of_pages)
						print "<script>top.location='".$self."'</script>";
				}
			}
			if($current_page!=1)
			{
				$previous = $current_page-1;
				echo "<a larger' href='".$self.$previous."'><b>&laquo;</b></a>";
			}
			
			$x=$current_page;
			
			if($current_page+3>$total_no_of_pages)
				if($total_no_of_pages-3>0)
					$x=$total_no_of_pages-3;
				else if($total_no_of_pages-2>0)
					$x=$total_no_of_pages-2;
				else if($total_no_of_pages-1>0)
					$x=$total_no_of_pages-1;
			
			for($i=$x;$i<=$x+3;$i++)
			{
				if($i==$current_page)
					print '<span class="active"><b>'.$i."</b></span>";
				else if($i>$total_no_of_pages)
					break;
				else
					echo "<a href='".$self.$i."'><b>".$i."</b></a>";
			}
			if($current_page!=$total_no_of_pages)
			{
				$next=$current_page+1;
				echo "<a href='".$self.$next."'><b>&raquo;</b></a>";
				//echo "<a href='".$self.$total_no_of_pages."'><b>".$last."</b></a>";
			}
			?></div></div><?php
		}
	}
}