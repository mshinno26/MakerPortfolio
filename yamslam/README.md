Yamslam
I produced a digital version of a board game called Yamslam. It is an object-oriented
Python application (see Yamslam_code) that includes a modular engine, as well as a GUI
container (see Yamslam_video); through this project, I learned about object-oriented
programming, modularization, and the PyGame library. I used data structures such as
dictionaries (for chips) and lists (for dice and players). All icons (see Yamslam_code, page 16)
were created using Gimp.
The algorithm at the heart of this application lies in the Pattern class (see Yamslam_code,
pages 5-8). A Pattern object has a rolls, counts, and patterns lists, populated using the
constructor, a “counting” method, and seven “pattern” methods. The counting method iterates
through the list of dice to the frequency of each number (how many ones and how many twos,
etc.), and saves these frequencies to a global list. This method is essential to more efficiently
check for patterns, especially because the order of the dice is unimportant. Each pattern method
checks the frequencies of each number (calculated by the counting method) for a different
scoreable hand and adds it to a dictionary. For example, the two_pairs() method checks for two
pairs of numbers (for example, two threes and two fives, or four sixes) by checking the list of
frequencies created by get_counts(). If any number shows up four times, the function
immediately adds the two-pair hand to the list of possible patterns. If any number shows up at
least twice, the two_pairs() increments the number of pairs found. If no four-of-a-kind has been
found after checking all six frequencies, the method then checks the number of pairs found—if
there are at least two, the method adds the two-pair hand to the list of possible patterns. This
method needs to check for a frequency of four, because the player might not be able to choose
“four of a kind” if that chip runs out. In this case, the player may choose two pairs. The method
does not need to check for a frequency of five, because the object will have already checked for a
Yamslam (five-of-a-kind). If one is found, all chips will automatically be available, anyway. The
Yamslam engine (see Yamslam_code, pages 9-11) can get the Pattern object’s list of patterns by
calling getPatterns(), which first updates the list by calling the previously mentioned counting
and pattern methods before returning self._patterns.
I created the Yamslam engine (see in Yamslam_code, pages 5-11: pattern.py, player.py,
yamslam.py) modularly, so that I could implement multiple types of user interfaces. No
references to any interfaces are present in these classes; instead, the objects deal completely with
the abstract data they have or are. At first, I used a terminal-based container that communicated
with the user via terminal print() and input(). Later on, I decided to create a graphical user
interface for the application—these classes, unlike the engine classes, include GUI references
such as position, surfaces, and media files (see Yamslam_code, 1-4, 8-9, 11-15: button.py,
chip.py, dice.py, playerScore.py, yamGuiUtil.py, and yamslam_gui.py). Due to the modular
nature of my program, I did not need to edit the engine code; instead, I simply replaced the
terminal container classes with PyGame-based classes. If desired, I could have similarly added
web, mobile, or tangible user interfaces.
