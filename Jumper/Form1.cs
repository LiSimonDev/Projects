using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Http.Headers;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Jumper
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        int game = 1;
        int playerJumpSpeed = 3;
        int playerSpeed = 3;
        int gravity_power = 1;
        int jump_speed = 1;
        int jump_speed1 = 1;
        Random rnd = new Random();
        int x=382, y=350, z=154;
        int CountDown = 5;
        int level = 0;

        private void LeftMoveTimer_Tick(object sender, EventArgs e)
        {
            if (Player.Left > 2)
            {
                Player.Left -= playerSpeed;
            }
        }

        private void RightMoveTimer_Tick(object sender, EventArgs e)
        {
            if (Player.Right < 583)
            {
                Player.Left += playerSpeed;
            }
        }

        private void JumpMoveTimer_Tick(object sender, EventArgs e)
        {
            jump_speed++;
            if (jump_speed > 3)
                jump_speed = 1;
            if (Player.Top > 20)
            {
                Player.Top -= playerJumpSpeed;
                if (Player.Top > 20)
                {

                    if (jump_speed == 3)
                    {
                        JumpMoveTimer.Interval += 1;
                        jump_speed = 1;
                    }
                    
                }
                if (JumpMoveTimer.Interval > 30)
                {
                    playerJumpSpeed = 0;
                }



            }


        }

        private void Gravity_Tick(object sender, EventArgs e)
        {
            jump_speed1++;
            if (jump_speed1 > 1)
                jump_speed1 = 1;
            if (Player.Top < 435)
            {
                if (Gravity.Interval > 1)
                {
                    if (jump_speed1 == 1)
                    {
                        jump_speed1 = 1;
                        Gravity.Interval -= 1;
                        label1.Text = Convert.ToString(Gravity.Interval);
                    }
                }



                Player.Top += gravity_power;
            }
            else
            {
                Gravity.Interval = 50;
                JumpMoveTimer.Interval = 5;
                playerJumpSpeed = 3;
            }

        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            if (game == 1)
            {
                if (e.KeyCode == Keys.D)
                {
                    RightMoveTimer.Start();
                }

                if (e.KeyCode == Keys.W)
                {
                    JumpMoveTimer.Start();
                }

                if (e.KeyCode == Keys.A)
                {
                    LeftMoveTimer.Start();
                }

                if (e.KeyCode == Keys.G)
                {
                    Gravity.Start();
                }
            }

        }

        private void Form1_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.D)
            {
                RightMoveTimer.Stop();
            }

            if (e.KeyCode == Keys.W)
            {
                JumpMoveTimer.Stop();
            }

            if (e.KeyCode == Keys.A)
            {
                LeftMoveTimer.Stop();
            }
        }

        private void GenerateObject_Tick(object sender, EventArgs e)
        {
            if (CountDown == 0)
            {
                x = rnd.Next(100 - level, 400 + level);
                y = rnd.Next(300 - level*2, 400);
                level++;
                this.pictureBox1.Location = new System.Drawing.Point(x, y);
                if (level < 4)
                {
                    CountDown = 5 - level;
                }
                else
                {
                    CountDown = 1;
                    this.pictureBox1.Size = new System.Drawing.Size(z, 31);
                    if (z > 50)
                    {
                        z -= 10;
                    }
                }

                label.Text = Convert.ToString("Level "+level);
            }
            CountDown--;
            label2.Text = Convert.ToString(CountDown);
            if (level > 4)
            {
                label2.Text = "FRENZY!";
            }


        }


        private void Check_Tick(object sender, EventArgs e)
        {
            if (Player.Top > y - 25 && Player.Top < y + 31 && Player.Left > x - 25 && Player.Left < x + z)
            {
                JumpMoveTimer.Interval = 5;
                playerJumpSpeed = 3;
                Gravity.Interval = 51;
                gravity_power = 0;
            }
            else
            {
                gravity_power = 1;
            }
            if(Player.Top>430)
            {
                GameOver();
            }
        }

        void GameOver()
        {
            game = 0;
            Check.Stop();
            GenerateObject.Stop();
            label2.Text = "GAME OVER";
            button1.Visible = false;
        }


    }
}
