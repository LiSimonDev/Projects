
class character //class for making heroes and enemies
{
	constructor(r1, r2, r3, r4)
	{
		this.health=r1;
		this.mana=r2;
		this.attack=r3;
		this.armor=r4;
	}
}

class item //class for making items
{
	constructor(hp, mp, ad, ar, desc, name)
	{
		this.hp;
		this.mp;
		this.ad;
		this.ar;
		this.desc;
		this.name;
	}
}
	
var inventory=[15];
shop_item=[5];
	
var charac=new character(500, 500, 100, 50); //main character stats
var charac_max=new character(500, 500, 100, 50);

for(var i=0; i<15; i++) //sets equipment slots
{
	inventory[i]=new item(); 
	inventory[i].hp=0;
	inventory[i].mp=0;
	inventory[i].ad=0;
	inventory[i].ar=0;
	inventory[i].desc="Nothing to see here";
	inventory[i].name="";
}

	inventory[0].hp=10000;
	inventory[0].mp=10000;
	inventory[0].ad=10000;
	inventory[0].ar=10000;
	inventory[0].desc="Legendary blade forged by devs";
	inventory[0].name="Zenith";
	

var r1, r2, r3, r4; //for random numbers
var action_window_text=document.getElementById("action_text").innerHTML; //declaring text manipulating variable
var action_window;
var action_content;

r1=(Math.round(Math.random() * 1000));
r2=(Math.round(Math.random() * 1000));
r3=(Math.round(Math.random() * 100));
r4=(Math.round(Math.random() * 50));

var e=new character(r1, r2, r3, r4);
var e_1=new character(r1, r2, r3, r4); //random enemy
var gold=50;
var fight=1;
var item_no=0;
var mpu=+10;
var score=0;
var buy_item;
var defeated_enemy_count=0;


var last_item_hp=0;
var last_item_mp=0;
var last_item_ad=0;
var last_item_ar=0;
var last_item_name="";
var last_item_id=(-1);


function set_stats() //updates character stats in html
{
	document.getElementById("health").innerHTML=charac.health+"/"+charac_max.health;
	document.getElementById("mana").innerHTML=charac.mana+"/"+charac_max.mana;
	document.getElementById("attack").innerHTML=charac.attack+"/"+charac_max.attack;
	document.getElementById("armor").innerHTML=charac.armor+"/"+charac_max.armor;
}

function enemy_set_stats() //updates enemy stats in html
{
	document.getElementById("enemy_health").innerHTML="HP: "+e.health+"/"+e_1.health;
	document.getElementById("enemy_mana").innerHTML="MP: "+e.mana+"/"+e_1.mana;
	document.getElementById("enemy_attack").innerHTML="AD: "+e.attack+"/"+e_1.attack;
	document.getElementById("enemy_armor").innerHTML="AR: "+e.armor+"/"+e_1.armor;
}

function punch(enemy_health)
{
	rand=random_attack(80, 120)/100;
	if(fight==1)
	{
	e.health-=Math.round(charac.attack*rand-e.armor/4);
	document.getElementById("action_text").innerHTML=action_window_text + "<span style='color:green'>You deal " + Math.round(charac.attack*rand-e.armor/4) + "HP.</span><br>";	
	action_window_text=document.getElementById("action_text").innerHTML;
	enemy_set_stats();
	result();
	}
	if(fight==1)
	{
	enemy_turn();
	slide_text();
	result();
	}
}

function fireball()
{
	mpu=document.getElementById("mana_precentage").value;
	rand=random_attack(80, 120)/100;
	if(fight==1)
	{
	e.health-=Math.round((charac.attack/50)*(Math.sqrt(charac.mana*mpu/10))*rand-e.armor/8);
	var helper=Math.round((charac.attack/50)*(Math.sqrt(charac.mana*mpu/10))*rand-e.armor/8);
	charac.mana-=Math.round(charac.mana*mpu/100);
	document.getElementById("action_text").innerHTML=action_window_text + "<span style='color:green'>You deal " + helper + "HP with fire damage.</span><br>";	
	action_window_text=document.getElementById("action_text").innerHTML;
	set_stats();
	enemy_set_stats();
	result();
	}
	if(fight==1)
	{
	enemy_turn();
	slide_text();
	result();
	}
}

function open_eq() //shows equipment
{
	document.getElementById("moves").innerHTML="<div class='eq_slot' id='item0' onclick='desc(0)'></div> <div class='eq_slot' id='item1' onclick='desc(1)'></div> <div class='eq_slot' id='item2' onclick='desc(2)'></div> <div class='eq_slot' id='item3' onclick='desc(3)'></div> <div class='eq_slot' id='item4' onclick='desc(4)'></div> <div class='eq_slot' id='item5' onclick='desc(5)'></div> <div class='eq_slot' id='item6' onclick='desc(6)'></div> <div class='eq_slot'  id='item7' onclick='desc(7)'></div> <div class='eq_slot' id='item8' onclick='desc(8)'></div> <div class='eq_slot' id='item9' onclick='desc(9)'></div> <div class='eq_slot' id='item10' onclick='desc(10)'></div> <div class='eq_slot' id='item11' onclick='desc(11)'></div> <div class='eq_slot' id='item12' onclick='desc(12)'></div> <div class='eq_slot' id='item13' onclick='desc(13)'></div> ";
	for(var i=0; i<14; i++)
	document.getElementById("item"+i).innerHTML="<br>"+inventory[i].name+"<br>";
	popup();
}

function desc(no_of_item)
{
	document.getElementById("item_stats").innerHTML=inventory[no_of_item].name+"<br>"+inventory[no_of_item].hp+"<br>"+inventory[no_of_item].mp+"<br>"+inventory[no_of_item].ad+"<br>"+inventory[no_of_item].ar+"<br>"+inventory[no_of_item].desc+"<br><div id='but'><input type='Button' value='Equip' onclick='equip()'></div>";	
	item_no=no_of_item;
}

function shop_desc(no_of_item)
{
	document.getElementById("item_stats").innerHTML=shop_item[no_of_item].name+"<br>"+shop_item[no_of_item].hp+"<br>"+shop_item[no_of_item].mp+"<br>"+shop_item[no_of_item].ad+"<br>"+shop_item[no_of_item].ar+"<br>"+shop_item[no_of_item].desc+"<br><div id='but'><input type='Button' value='Buy' onclick='buy()'></div><br>";	
	item_no=no_of_item;
	buy_item=no_of_item;
}

function buy()
{
	for(var i=0; i<15; i++)
	{
		if(inventory[i].name=="")
		{
			inventory[i].hp=shop_item[buy_item].hp;
			inventory[i].mp=shop_item[buy_item].mp;
			inventory[i].ad=shop_item[buy_item].ad;
			inventory[i].ar=shop_item[buy_item].ar;
			inventory[i].desc=shop_item[buy_item].desc;
			inventory[i].name=shop_item[buy_item].name;
			open_eq();
			break;
		}
		else if(i==14)
		{
			document.getElementById("action_text").innerHTML=action_window_text+"No inventory space<br>";
			action_window_text=document.getElementById("action_text").innerHTML;
			slide_text();
			document.getElementById("action_text").innerHTML=action_window_text+"<div id='but'><input type='Button' value='Back' onclick=fight_window()></div> <div id='but'><input type='Button' value='???' onclick=''></div>";
			
		}
	}
}

function equip()
{
	if(last_item_id>(-1))
		inventory[last_item_id].name=last_item_name;
	last_item_id=item_no;
	
	charac.health-=last_item_hp;
	charac.mana-=last_item_mp;
	charac.attack-=last_item_ad;
	charac.armor-=last_item_ar;
	
	charac.health+=inventory[item_no].hp;
	charac.mana+=inventory[item_no].mp;
	charac.attack+=inventory[item_no].ad;
	charac.armor+=inventory[item_no].ar;
	
	charac_max.health-=last_item_hp;
	charac_max.mana-=last_item_mp;
	charac_max.attack-=last_item_ad;
	charac_max.armor-=last_item_ar;
	
	charac_max.health+=inventory[item_no].hp;
	charac_max.mana+=inventory[item_no].mp;
	charac_max.attack+=inventory[item_no].ad;
	charac_max.armor+=inventory[item_no].ar;
	
	last_item_hp=inventory[item_no].hp;
	last_item_mp=inventory[item_no].mp;
	last_item_ad=inventory[item_no].ad;
	last_item_ar=inventory[item_no].ar;
	
	last_item_name=inventory[item_no].name;
	inventory[item_no].name=inventory[item_no].name+"(E)";
	
	set_stats();
	open_eq();
}	

function open_skills() //show skills
{
	document.getElementById("moves").innerHTML="<div id='but'><input type='Button' id='buut' value='Punch' onclick='punch(e.health)'></div><div id='but'><input type='Button' id='buut' value='Fireball' onclick='fireball()'></div><div id='but'><input type='Button' id='buut' value='???' onclick=''></div><div id='but'><input type='Button' id='buut' value='???' onclick=''></div><div id='but'><input type='Button' id='buut' value='???' onclick=''></div><div id='but'><input type='text' id='mana_precentage' value='10' class='mana_precentage'><p class='textt'>Mana precentage per spell, not physical</p></div>";
}

function slide_text() //limits action text lines to 5
{
	if(action_window_text.split("<br>").length>5)//number of lines in action window
	{									
	do
	{
		b=action_window_text.split("<br>");
		var c=b.slice(1);
		action_window_text=c.join("<br>");
		document.getElementById("action_text").innerHTML=action_window_text;
	}while(action_window_text.split("<br>").length>5);
	}
}

function result() //checks outcome of battle
{
	if(e.health<=0)	
		won_battle();
	else if(charac.health<=0)
		lost_battle();
}

function enemy_turn() 
{
	rand_e=random_attack(80, 120)/100;
	charac.health-=Math.round(e.attack*rand_e-charac.armor/4);
	set_stats();
	document.getElementById("action_text").innerHTML=action_window_text + "You lost " +Math.round(e.attack*rand_e-charac.armor/4) + "HP.<br>";
	action_window_text=document.getElementById("action_text").innerHTML;
}

function random_enemy() //randomizes enemy stats
{
	e.health=(Math.round(Math.random() * 1000));
	e.mana=(Math.round(Math.random() * 100));
	e.attack=(Math.round(Math.random() * 100));
	e.armor=(Math.round(Math.random() * 10));
	
	e_1.health=e.health;
	e_1.mana=e.mana;
	e_1.attack=e.attack;
	e_1.armor=e.armor;
	document.getElementById("action_text").innerHTML=action_window_text + "New enemy approaches!<br>";
	action_window_text=document.getElementById("action_text").innerHTML;
	slide_text();
	fight=1;
	enemy_set_stats();
}

function random_attack(min, max)
{
	return Math.round(min + (max - min)*Math.random());
}

function won_battle() 
{
	score+=Math.round(e_1.health/100+e_1.mana/100+e_1.attack/10+e_1.armor/10);
	document.getElementById("gold").innerHTML="Gold: "+(gold+=50);
	fight=0;
	document.getElementById("action_text").innerHTML=action_window_text + "Congratulation, you won!<br>";
	action_window_text=document.getElementById("action_text").innerHTML;
	slide_text();
	document.getElementById("action_text").innerHTML=action_window_text + "<div id='but'><input type='Button' value='Shop' onclick=open_shop()></div> <div id='but'><input type='Button' value='Continue' onclick='remove_buttons(), random_enemy()'></div>";
	document.getElementById("score").innerHTML=score;
	
	defeated_enemy_count++;
	charac.health+=0.1*charac_max.health;
	charac.mana+=0.1*charac_max.mana;
	if(charac.health>charac_max.health)
		charac.health=charac_max.health;
	if(charac.mana>charac_max.mana)
		charac.mana=charac_max.mana;
	set_stats();

}

function remove_buttons()
{
	document.getElementById("action_text").innerHTML=action_window_text;
}

function lost_battle()
{
	fight=0;
	document.getElementById("action_text").innerHTML=action_window_text + "You are ded<br>";
	action_window_text=document.getElementById("action_text").innerHTML;
	document.getElementById("action_text").innerHTML=action_window_text + "<div id='but'> <div id='but'><input type='Button' value='Continue' onclick=location.reload()></div>";
}

function popup() {  //item popup and more
    $(".eq_slot").click(function(){
       $('.hover_bkgr_fricc').show();
    });
    $('.hover_bkgr_fricc').click(function(){
        $('.hover_bkgr_fricc').hide();
    });
    $('.popupCloseButton').click(function(){
        $('.hover_bkgr_fricc').hide();
    });
};

function open_shop()
{
	for(var i=0; i<5; i++) //sets equipment slots
{
	shop_item[i]=new item(); 
	shop_item[i].hp=0;
	shop_item[i].mp=0;
	shop_item[i].ad=0;
	shop_item[i].ar=0;
	shop_item[i].desc="Shopkeeper's tool";
	shop_item[i].name="Weapon" + i;
}

	document.getElementById("action_text").innerHTML=action_window_text+"Welcome to my shop, what would you like to buy? <br>";
	action_window_text=document.getElementById("action_text").innerHTML;
	slide_text();
	document.getElementById("action_text").innerHTML=action_window_text+"<div id='but'><input type='Button' value='Back' onclick=fight_window()></div> <div id='but'><input type='Button' value='???' onclick=''></div>";
	action_content=document.getElementById("action_content").innerHTML;
	document.getElementById("action_content").innerHTML="<div class='eq_slot' id='item_shop0' onclick='shop_desc(0)'></div> <div class='eq_slot' id='item_shop1' onclick='shop_desc(1)'></div> <div class='eq_slot' id='item_shop2'onclick='shop_desc(2)'></div> <div class='eq_slot' id='item_shop3' onclick='shop_desc(3)'></div> <div class='eq_slot' id='item_shop4' onclick='shop_desc(4)'></div>";

for(var i=0; i<5; i++)
	document.getElementById("item_shop"+i).innerHTML="<br>"+shop_item[i].name+"<br>";

	open_eq();
}

function fight_window()
{
	document.getElementById("action_text").innerHTML=action_window_text;
	document.getElementById("action_content").innerHTML=action_content;
	random_enemy();
	open_skills();
}

enemy_set_stats();
set_stats();
popup();

