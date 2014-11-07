Title: Getting Divvy-like functionality on Linux
Date: 2011-11-18 16:49
Author: Danny Hermes (noreply@blogger.com)
Tags: Compiz, Divvy, Linux, Mac OS X, Window Manager
Slug: getting-divvy-like-functionality-on-linux

I **love** my [Divvy](http://mizage.com/divvy), as I'm sure many do, but
it's not available for Linux. (I completely understand why it isn't,
though the fact that they make Divvy a **free** demo with full
functionality brings into question how much they are trying to monetize
it.) Anyhow, not wanting to give away my left hand for a personal
computer, I run Ubuntu on my home machine (but OS X at work, kind of
funny).  
  
In reality, all I really need from Divvy is the ability to do three
things without the mouse that I normally couldn't do.  
1. Maximize a window  
2a. Make the window take the entire left half of the screen  
2b. Make the window take the entire right half of the screen  
That's all, I'm not asking for much.  
  
=====================================================================  
=====================================================================  
=====================================================================  
As a brief side not for those who don't know, with Divvy, I start with a
window  

<div class="separator" style="clear: both; text-align: center;">

[![](http://1.bp.blogspot.com/-lc3LxjbwMgE/Tg37-n6sMzI/AAAAAAAAAuM/aG0axItwtQQ/s640/divvy_before.png)](http://1.bp.blogspot.com/-lc3LxjbwMgE/Tg37-n6sMzI/AAAAAAAAAuM/aG0axItwtQQ/s1600/divvy_before.png)

</div>

<div class="separator" style="clear: both; text-align: left;">

and then call up Divvy with (a command I set globally) Ctrl-Z

</div>

<div class="separator" style="clear: both; text-align: center;">

[![](http://3.bp.blogspot.com/-ZhSgb0G1zS4/Tg37_BoIH7I/AAAAAAAAAuQ/wbo8CeADeoE/s640/divvy_calldivvy.png)](http://3.bp.blogspot.com/-ZhSgb0G1zS4/Tg37_BoIH7I/AAAAAAAAAuQ/wbo8CeADeoE/s1600/divvy_calldivvy.png)

</div>

<div class="separator" style="clear: both; text-align: left;">

and then once Divvy is up, I just hit the letter L (another command I
made) and voila

</div>

<div class="separator" style="clear: both; text-align: center;">

[![](http://1.bp.blogspot.com/-lgkfOfCcBhk/Tg37-Saf4qI/AAAAAAAAAuI/WEC8-drLJnw/s640/divvy_after.png)](http://1.bp.blogspot.com/-lgkfOfCcBhk/Tg37-Saf4qI/AAAAAAAAAuI/WEC8-drLJnw/s1600/divvy_after.png)

</div>

<div class="separator" style="clear: both; text-align: left;">

my window is on the full left half of the screen.

</div>

<div
style="margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px;">

=====================================================================

</div>

<div
style="margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px;">

=====================================================================

</div>

<div
style="margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px;">

=====================================================================  
  
So, every other weekend for the last five months, I have tried to find a
Divvy-like solution for Linux. I picked up and discarded Bluetile and
PyWO along the way, the former because it is way too heavy a solution
and the latter because it required the keypad, which my laptop keyboard
does not have (of course I could've enabled NumLock to simulate the
keypad, but that is too big a PITA).  
  
Finally, last night I came to a solution that I want to share (in case
anyone has gone through the pain I have). That solution is Compiz and
here is how I did it:  
1. Install Compiz from the command line via <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">sudo
apt-get install compizconfig-settings-manager</span>  
2. Install the extra plugins via <span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">sudo
apt-get install compiz-fusion-plugins-extra</span>  
3. Open Compiz (<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">ccsm</span>
from the command line) or  
<div class="separator" style="clear: both; text-align: center;">

[![](http://2.bp.blogspot.com/-WwT5-TlObGI/Tg396R7x70I/AAAAAAAAAuo/iThwNYW9IAU/s640/ccsm.png)](http://2.bp.blogspot.com/-WwT5-TlObGI/Tg396R7x70I/AAAAAAAAAuo/iThwNYW9IAU/s1600/ccsm.png)

</div>

4. Go into the Window Management subsection  
<div class="separator" style="clear: both; text-align: center;">

[![](http://2.bp.blogspot.com/-wc2kZtUMaHQ/Tg3-S3heFZI/AAAAAAAAAus/AeNaALZuhro/s640/window_manage.png)](http://2.bp.blogspot.com/-wc2kZtUMaHQ/Tg3-S3heFZI/AAAAAAAAAus/AeNaALZuhro/s1600/window_manage.png)

</div>

5. Enter Grid and set the "Put Left" and "Put Right" bindings to Alt-F8
and Alt-F9, while disabling everything else (my choice, doesn't have to
be yours, if you have a Keypad on your keyboard and NumLock is not going
to interfere with the letter 'm', then go for it)  
<div class="separator" style="clear: both; text-align: center;">

[![](http://4.bp.blogspot.com/-93KYvNN8K4E/Tg3-n-GpXdI/AAAAAAAAAuw/GFQ79_bEcOI/s640/grid.png)](http://4.bp.blogspot.com/-93KYvNN8K4E/Tg3-n-GpXdI/AAAAAAAAAuw/GFQ79_bEcOI/s1600/grid.png)

</div>

(Also, another side note, if you are having trouble figuring out how to
change the binding, just click the first box, the ones that say Disabled
or whatever the current binding is and then "Grab Key Combination"  
<div class="separator" style="clear: both; text-align: center;">

[![](http://4.bp.blogspot.com/-HD3wWGZ-BHI/Tg3_BUZc8LI/AAAAAAAAAu0/Pv_Cd1YxeMg/s640/set_val.png)](http://4.bp.blogspot.com/-HD3wWGZ-BHI/Tg3_BUZc8LI/AAAAAAAAAu0/Pv_Cd1YxeMg/s1600/set_val.png)

</div>

<div class="separator" style="clear: both; text-align: left;">

to change the binding to your hearts content.)

</div>

  
7. For maximize go to General Options  
<div class="separator" style="clear: both; text-align: center;">

[![](http://2.bp.blogspot.com/-GE1EdZum6uU/Tg3_Mb_lsbI/AAAAAAAAAu4/m7LZxmpMmgo/s640/general.png)](http://2.bp.blogspot.com/-GE1EdZum6uU/Tg3_Mb_lsbI/AAAAAAAAAu4/m7LZxmpMmgo/s1600/general.png)

</div>

8. In the Key Bindings tab, make sure "Toggle Window Maximized" is set
to it's default value of Alt-F10  
  
<div class="separator" style="clear: both; text-align: center;">

[![](http://3.bp.blogspot.com/-cFTNsGgN7gY/Tg3_dJYFduI/AAAAAAAAAu8/hAagDN6UB0w/s640/maximize.png)](http://3.bp.blogspot.com/-cFTNsGgN7gY/Tg3_dJYFduI/AAAAAAAAAu8/hAagDN6UB0w/s1600/maximize.png)

</div>

<div class="separator" style="clear: both; text-align: left;">

  

</div>

<div class="separator" style="clear: both; text-align: left;">

So with that, I my conditions satisfied: 1. via Alt-F10, 2a. via Alt-F8
and 2b. via Alt-F9. My search is over (for now...unless I make
DivvyBuntu...)

</div>

<div class="separator" style="clear: both; text-align: left;">

  

</div>

(A little bit more about what you can do with Compiz:  
  
  
  
  
<center>
</center>
  
Linux nerds watch Las Vegas, told you so Brent!)

</div>

[About Bossy Lobster](https://profiles.google.com/114760865724135687241)

</p>

