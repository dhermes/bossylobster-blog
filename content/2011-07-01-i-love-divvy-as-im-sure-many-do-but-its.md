---
title: Getting Divvy-like functionality on Linux
date: 2011-07-01
author: Danny Hermes (dhermes@bossylobster.com)
tags: Compiz, Divvy, Linux, Mac OS X, Window Manager
slug: i-love-divvy-as-im-sure-many-do-but-its
comments: true
github_slug: content/2011-07-01-i-love-divvy-as-im-sure-many-do-but-its.md
---

I **love** my [Divvy](http://mizage.com/divvy), as I'm sure many do, but
it's not available for Linux. (I completely understand why it isn't,
though the fact that they make Divvy a **free** demo with full
functionality brings into question how much they are trying to monetize
it.) Anyhow, not wanting to give away my left hand for a personal
computer, I run Ubuntu on my home machine (but OS X at work, kind of
funny).

In reality, all I really need from Divvy is the ability to do three
things without the mouse that I normally couldn't do.

- (1.) Maximize a window
- (2a.) Make the window take the entire left half of the screen
- (2b.) Make the window take the entire right half of the screen

That's all, I'm not asking for much.

---------------------------------------------------------------------

As a brief side not for those who don't know, with Divvy, I start with a
window

<div markdown="1" style="text-align: center;">
  ![Before Re-sizing with Divvy](/images/divvy_before.png)
</div>

and then call up Divvy with (a command I set globally) Ctrl-Z

<div markdown="1" style="text-align: center;">
  ![Divvy Menu](/images/divvy_calldivvy.png)
</div>

and then once Divvy is up, I just hit the letter L (another command I
made) and voil&#0224;

<div markdown="1" style="text-align: center;">
  ![After Re-sizing with Divvy](/images/divvy_after.png)
</div>

my window is on the full left half of the screen.

---------------------------------------------------------------------

So, every other weekend for the last five months, I have tried to find a
Divvy-like solution for Linux. I picked up and discarded Bluetile and
PyWO along the way, the former because it is way too heavy a solution
and the latter because it required the keypad, which my laptop keyboard
does not have (of course I could've enabled NumLock to simulate the
keypad, but that is too big a PITA).

Finally, last night I came to a solution that I want to share (in case
anyone has gone through the pain I have). That solution is Compiz and
here is how I did it:

1.  Install Compiz from the command line via

        sudo apt-get install compizconfig-settings-manager

1.  Install the extra plugins via

        apt-get install compiz-fusion-plugins-extra

1.  Open Compiz (`ccsm` from the command line) or
    <div markdown="1" style="text-align: center;">
       ![CompixConfig Settings Manager](/images/ccsm.png)
    </div>

1.  Go into the Window Management subsection
    <div markdown="1" style="text-align: center;">
       ![Window Management Settings](/images/window_manage.png)
    </div>

1.  Enter Grid and set the "Put Left" and "Put Right" bindings to Alt-F8
    and Alt-F9, while disabling everything else (my choice, doesn't have to
    be yours, if you have a Keypad on your keyboard and NumLock is not going
    to interfere with the letter 'm', then go for it)
    <div markdown="1" style="text-align: center;">
      ![Grid Settings](/images/grid.png)
    </div>
    (Also, another side note, if you are having trouble figuring out how to
    change the binding, just click the first box, the ones that say Disabled
    or whatever the current binding is and then "Grab Key Combination"
    <div markdown="1" style="text-align: center;">
      ![Set Shortcut Value](/images/set_val.png)
    </div>
    to change the binding to your hearts content.)

1.  For maximize go to General Options
    <div markdown="1" style="text-align: center;">
      ![General Compiz Settings](/images/general.png)
    </div>

1.  In the Key Bindings tab, make sure "Toggle Window Maximized" is set
    to it's default value of Alt-F10
    <div markdown="1" style="text-align: center;">
      ![Maximize Command](/images/maximize.png)
    </div>

---------------------------------------------------------------------

So with that, my conditions are satisfied:

- Condition (1.) via Alt-F10
- Condition (2a.) via Alt-F8
- Condition (2b.) via Alt-F9

My search is over (for now...unless I make DivvyBuntu...)
