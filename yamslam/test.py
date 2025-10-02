from pattern import Pattern as pattern

rolls = []

for i in range(5):
    rolls.append(int(input("Roll: ")))

p = pattern(rolls)
print("yamslam: ", p.yammerslammer())
print("large: ", p.large())
print("four: ", p.four_of_a_kind())
print("full: ", p.full_house())
print("flush: ", p.flush())
print("small: ", p.small())
print("three: ", p.three_of_a_kind())
print("twopairs: ", p.two_pairs())