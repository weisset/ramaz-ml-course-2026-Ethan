"""HW00 — Python Bootcamp: Implementation

Complete the functions below. Each function has a docstring describing
what it should do, along with examples. Run `uv run pytest` to check
your work, and `uv run python score.py` to see your current grade.
"""

from __future__ import annotations

from typing import Callable

# ── Part 1: Lists ─────────────────────────────────────────────────────────────


def flatten(nested: list[list]) -> list:
    """Return a single flat list from a list of lists.

    Examples:
        >>> flatten([[1, 2], [3, 4], [5]])
        [1, 2, 3, 4, 5]
        >>> flatten([[], [1]])
        [1]
        >>> flatten([])
        []
    """
    return [item for subList in nested for item in subList]
    """
    Ethan's Notes:
    having item before the for is the same as .append(item)
    if it were item*2 then it's the same as .append(item*2) which would double each value
    so first we find the first item in the main list
    then we iterate through it, if it's not a sublist and just one value then we only append that
    and each item we iterate through in the sublist is appended to the flattened list we are making
    """
    # raise NotImplementedError("Implement flatten()")


def most_frequent(items: list) -> object:
    """Return the element that appears most often in items.

    If there is a tie, returning any one of the tied elements is fine.
    Raise ValueError if items is empty.

    Examples:
        >>> most_frequent([1, 2, 2, 3])
        2
        >>> most_frequent(['a', 'b', 'a', 'c', 'a'])
        'a'
    """
    if len(items) == 0:
        raise ValueError

    maxCount = 0
    for element in set(items):
        tempCount = items.count(element)
        if tempCount > maxCount:
            maxCount = tempCount
            maxElement = element

    return maxElement
    """
    Ethan's Notes:
    set gets rid of all dupes, makes it easier to iterate through each unique element
    count function will tell you how many times a specified element appears in your list

    better version:
    just iterate through original list and have a counter for each unique element
    count goes up by one each time
    you also check each count increase to see if that element is the new most frequent
    """
    # raise NotImplementedError("Implement most_frequent()")


def running_average(numbers: list[float]) -> list[float]:
    """Return the cumulative average at each position.

    The i-th element of the result is the mean of numbers[0], ..., numbers[i].

    Examples:
        >>> running_average([10.0, 20.0, 30.0])
        [10.0, 15.0, 20.0]
        >>> running_average([4.0])
        [4.0]
        >>> running_average([])
        []
    """
    averages = []
    total = 0
    for position, element in enumerate(numbers, start=1):
        total += element
        averages.append(total / position)
    return averages
    """
    Ethan's Notes:
    enumerate makes it so each element in numbers is the value in a key-value pair
    the key assigned by enumerate is a counter for the position of each element in the iterable
    start=1 makes it so it starts counting at one
    so if you have [10.0, 15.0, 20.0] and use default start then each pair would be:
    0, 10.0
    1, 15.0
    2, 20.0
    and so by having it start at one you can easily divide by total elements in ur current avg
    so basically you update the total and then divide by number of elements so far
    then just append that
    """
    # raise NotImplementedError("Implement running_average()")


def chunk(items: list, size: int) -> list[list]:
    """Split items into sublists of length size.

    The last sublist may be shorter if len(items) is not divisible by size.

    Examples:
        >>> chunk([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> chunk([1, 2, 3], 3)
        [[1, 2, 3]]
        >>> chunk([], 4)
        []
    """
    return [items[i : i + size] for i in range(0, len(items), size)]
    """
    Ethan's Notes:
    making a list where we append a list starting at position i and ending 1 position before i+size
    because list[a:b] returns a list made of the elements in list starting at position a (inclusive)
    and ending at the element before position b (so it's exclusive)
    and then i increases every step by the value of size
    """
    # raise NotImplementedError("Implement chunk()")


def rotate(items: list, k: int) -> list:
    """Rotate items left by k positions.

    A negative k rotates right. If items is empty, return [].
    k larger than len(items) wraps around correctly.

    Examples:
        >>> rotate([1, 2, 3, 4, 5], 2)
        [3, 4, 5, 1, 2]
        >>> rotate([1, 2, 3], -1)
        [3, 1, 2]
        >>> rotate([1, 2, 3], 4)
        [2, 3, 1]
    """
    if not items:
        return items
    trueK = k % len(items)
    return items[trueK:] + items[:trueK]
    """
    Ethan's Notes:
    first there's the if to make sure that we don't get an error when items is empty
    because % (modulo) is division except it returns the remainder instead
    so dividing by zero still isn't allowed
    modulo is needed if k is further from 0 than len(items) (aka if |k| > |len(items)|)
    because if you try to slice a list starting at a position bigger than the list it won't wrap it
    instead it'll just return an empty list because if you start after the list there's nothing
    
    given a basic scenario where list is longer than k and k is positive:
    if you want to rotate a list 3 spaces to the left
    same as moving the item in position 3 (the 4th item) in the list to position 0 (the 1st item)
    and then position 4 to position 1 and so on
    that is represented by items[truek:]
    but then you still have to wrap and do the items from position 0 up until position 3
    and that's what items[:trueK] does
    and then the plus is to concatenate them
    """
    # raise NotImplementedError("Implement rotate()")


def run_length_encode(items: list) -> list[tuple]:
    """Compress consecutive identical elements into (count, value) tuples.

    Examples:
        >>> run_length_encode(['a', 'a', 'b', 'b', 'b', 'a'])
        [(2, 'a'), (3, 'b'), (1, 'a')]
        >>> run_length_encode([1, 2, 3])
        [(1, 1), (1, 2), (1, 3)]
        >>> run_length_encode([])
        []
    """
    if not items:
        return items

    lastElement = items[0]
    countConsec = 1
    rleItems = []
    for element in items[1:]:
        if element == lastElement:
            countConsec += 1
        else:
            rleItems.append((countConsec, lastElement))
            lastElement = element
            countConsec = 1
    rleItems.append((countConsec, lastElement))
    return rleItems
    """
    Ethan's Notes:
    Okay so this isn't the ideal version but it seems very much good enough, nothing like n^2 or wtv
    only inneficiency from my limited ai checking is items[1:] stores a separate list in memory
    we know that index 0 is equivalent to itself the so we can start at index 1 with countConsec = 1
    then we just keep checking if they're the same (no need to update lastElement if so)
    if it's different then we append a tuple with the double parens (()) cuz that's how it works
    then we reset last element and the count and go at it again
    but when we get to element at index -1 (aka finish the list) then we won't record it in the for
    that's because if it's still consecutive then we only up the count then exit the loop
    and if it's different then we append the previous consecutive elements but then exit the loop
    so that's why there's the extra append outside of the loop
    """
    # raise NotImplementedError("Implement run_length_encode()")


def sliding_window(items: list, size: int) -> list[list]:
    """Return all consecutive windows of length size.

    Each window overlaps with the previous one by size-1 elements.
    If len(items) < size, return [].

    Examples:
        >>> sliding_window([1, 2, 3, 4, 5], 3)
        [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
        >>> sliding_window([1, 2, 3], 2)
        [[1, 2], [2, 3]]
        >>> sliding_window([1, 2], 3)
        []
        >>> sliding_window([], 2)
        []
    """
    if size > len(items):
        return []
    return [
        items[windowStart : size + windowStart] for windowStart in range(0, len(items) - size + 1)
    ]
    """
    Ethan's Notes:
    first of all len(items) returns 0 if the list is empty so that's all good with the if statement
        allegedly don't need if statement because range will do the same thing in edge case but wtv
    have to return list of list btw so the slicing that gets appended already makes the sublist
    need range with len in case items isn't basic and doesn't just have 1 at index 0
    the range is the different positions (indices?) windowStart iterates through
        so this means our first slice will start at index 0
        and because where the range stops is exclusive we have the +1
        remember iterating through range gives us what index the window starts at
        so with first example 5-3+1 is 3 which means we stop after we do index 2
        which means the last window starts with the int 3 since that's at index 2
    so that explains windowsStart for items[windowStart:...]
    and then for where to stop the slice it's still exclusive
        so using the same example (first one):
        if windowStart is at 0 then the stop of the slice is at index 3
        but that actually means we do indices 0, 1, and 2
        which is 3 individual items, exactly our size
    """
    # raise NotImplementedError("Implement sliding_window()")


"""
Ethan's Section 1.1 Lists Notes
    Okay so overall pretty good answers as far as I can tell
    There's a few opportunities to make it better using more complicated dictionary/key-value pairs
    But I'd rather save that for the actual parts about dictionaries and sets
    I only did some more basic versions
    There is one heavily unoptimized answer (n^2 instead of n or wtv I kinda know what that means)
    And I think I could also maybe use enumerate in one of my other answers but it looked more
        complex than the other usage of enumerate and I think it's nice to really try to answer
        with my own knowledge mostly
    
    So yeah main thing I could improve on is probably going to be covered in dictionaries and sets
"""

# ── Part 2: Dictionaries ──────────────────────────────────────────────────────


def count_occurrences(items: list) -> dict:
    """Return a dict mapping each unique element to its count in items.

    Examples:
        >>> count_occurrences(['a', 'b', 'a', 'c', 'b', 'b'])
        {'a': 2, 'b': 3, 'c': 1}
        >>> count_occurrences([])
        {}
    """
    occurrencesDict = {}
    
    for element in items:
        occurrencesDict[element] = occurrencesDict.get(element, 0) + 1
    
    return occurrencesDict
    # raise NotImplementedError("Implement count_occurrences()")
    """
    Ethan's Notes:
    so first I make the dictionary both so i can call it and so I can return a blank one if needed
    then the idea is that i go through each element in items and do one of two things:
        if there is already a key value pair for that element in the dictionary then value += 1
        if there is no key for that element yet then a value of 0 is returned and then i add 1
    this happens because .get will check for that key, and return the value if it exists
    but if it doesn't exist it will return the value i put there, which is 0, not required tho
    and then we take that value of either 0 or whatever it is and add 1
    and we set the item with element as the key to have the value that i just increased
    and if the item doesn't exist yet then this makes it
    we iterate through the whole list then return the dictionary
    """

def invert_dict(d: dict) -> dict:
    """Return a new dict with keys and values swapped.

    Examples:
        >>> invert_dict({'a': 1, 'b': 2})
        {1: 'a', 2: 'b'}
    """
    return {value:key for key, value in d.items()}
    # raise NotImplementedError("Implement invert_dict()")
    """
    Ethan's Notes:
    so dictionary comprehension also exists
    doing .items will loop through keys and values together, so i can get them both at once
    so instead of for key in d and then doing d[key]:key which would check d again for value of key
    i just take the value when i'm already taking the key and then swapping them
    with list comprehension it would basically append what you had first
        for dictionaries to do its version of appending with dictionary comprehension
        you have to do it as key:value to append the pair
    so then just iterate through dictionary and do that but swap key and value when appending
    """


def group_by(items: list[dict], key: str) -> dict[str, list[dict]]:
    """Group a list of dicts by the value at the given key.

    Examples:
        >>> records = [
        ...     {'name': 'Alice', 'dept': 'Eng'},
        ...     {'name': 'Bob', 'dept': 'HR'},
        ...     {'name': 'Carol', 'dept': 'Eng'},
        ... ]
        >>> result = group_by(records, 'dept')
        >>> len(result['Eng'])
        2
        >>> len(result['HR'])
        1
    """
    groups = {}
    for d in items:
        groups.setdefault(d[key], []).append(d)
    return groups
    # raise NotImplementedError("Implement group_by()")
    """
    Ethan's Notes:
    iterate through list so we are going dictionary by dictionary
    .setdefault returns the value associated with d[key] just like .get
    but what makes it different from .get is that it won't just return [] if the pair doesn't exist
    instead, if the pair doesn't exist, it will create the pair d[key]: [] in groups
    and then returns that value []
    and then we append the dictionary we are looking at in items to that list
    and iterate through each dictionary in items, and if d[key] is the same as another dictionary
        then they are appended to the same list ofc
    then we return groups
    """


def deep_get(d: dict, path: str, default: object = None) -> object:
    """Retrieve a value from a nested dict using a dot-separated key path.

    Return default if any key along the path is missing.

    Examples:
        >>> deep_get({'a': {'b': {'c': 42}}}, 'a.b.c')
        42
        >>> deep_get({'a': 1}, 'a.b', default=-1)
        -1
        >>> deep_get({'x': 10}, 'y')  # returns None (default)
    """
    for key in path.split("."):
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d
    # raise NotImplementedError("Implement deep_get()")
    """
    Ethan's Notes:
    .split('.') means that we only look at any one segment of the string until we hit a .
    then we take that segmant and run the loop
    then we move to the next segment
    isinstance checks if d is the data type dict
    so if it's not a dictionary then we return default
    but if it is we get the value from the rest of the nested dictionary
    if we are still iterating but d is not a dictionary then we return default
    at the end we return d
    """


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Return indices (i, j) where nums[i] + nums[j] == target, with i < j.

    Return None if no such pair exists.

    Hint: There is an elegant O(n) solution using a dict. As you scan through
    nums, ask: "have I already seen the number I need to pair with this one?"

    Examples:
        >>> two_sum([2, 7, 11, 15], 9)
        (0, 1)
        >>> two_sum([3, 2, 4], 6)
        (1, 2)
        >>> two_sum([1, 2, 3], 100)
        None
    """
    seen = {}
    for i, n in enumerate(nums):
        if n <= target:
            try:
                return (seen[target - n], i)
            except KeyError:
                seen[n] = i
    return None
    # raise NotImplementedError("Implement two_sum()")
    """
    Ethan's Notes:
    Technically might not work if negative numbers get involved
    also try except might not be most optimal but i wanted to try it
    i think it's pretty self-explanatory code except enumerate which i've explained before
    """
"""
Ethan's Section 1.2 Dictionaries Notes
    we chilling ong
    shape lowk is cheating
"""

# ── Part 3: Sets ──────────────────────────────────────────────────────────────


def find_duplicates(items: list) -> set:
    """Return the set of elements that appear more than once in items.

    Examples:
        >>> find_duplicates([1, 2, 2, 3, 3, 3, 4])
        {2, 3}
        >>> find_duplicates([1, 2, 3])
        set()
        >>> find_duplicates([])
        set()
    """
    seen = set()
    dupes = set()
    for i in items:
        if i in seen:
            dupes.add(i)
        else:
            seen.add(i)
    return dupes
    # raise NotImplementedError("Implement find_duplicates()")
    """
    Ethan's Notes:
    make two sets, seen and dupes, iterate through list, if element in seen, add to dupes
    otherwise add to seen
    """

def jaccard_similarity(a: set, b: set) -> float:
    """Return |A intersection B| / |A union B|.

    Return 0.0 if both sets are empty.

    Examples:
        >>> jaccard_similarity({1, 2, 3}, {2, 3, 4})
        0.5
        >>> jaccard_similarity({1, 2}, {3, 4})
        0.0
        >>> jaccard_similarity(set(), set())
        0.0
    """
    try:
        return len(a & b) / len(a | b)
    except ZeroDivisionError:
        return 0.0
    # raise NotImplementedError("Implement jaccard_similarity()")
    """
    Ethan's Notes:
    union ( | ) combines all unique elements from both sets, so 123 and 345 is 12345 (no dupe 3)
    intersection ( & ) only elements in both sets, so 123 and 345 is 3
    """

"""
Ethan's Section 1.3 Set Notes:
    idk it's short
"""
# ── Part 4: Higher-order functions ────────────────────────────────────────────


def apply_twice(f: Callable, x: object) -> object:
    """Apply f to x, then apply f to the result: f(f(x)).

    Examples:
        >>> apply_twice(lambda n: n * 2, 3)
        12
        >>> apply_twice(str.upper, 'hello')
        'HELLO'
    """
    return f(f(x))
    # raise NotImplementedError("Implement apply_twice()")
    """
    Ethan's Notes
    kinda recursion? just have call a function and then call same function with that
    other call as its argument
    """

def make_multiplier(n: float) -> Callable[[float], float]:
    """Return a function that multiplies its argument by n.

    Each call to make_multiplier returns an independent function.

    Examples:
        >>> double = make_multiplier(2)
        >>> double(5)
        10.0
        >>> triple = make_multiplier(3)
        >>> triple(4)
        12.0
    """
    return lambda x: x * n
    # raise NotImplementedError("Implement make_multiplier()")
    """
    Ethan's Notes:
    lambda kinda makes a temp function that can take in arguments
    so lambda x: x * n means if you assign the output of make_multiplier to a variable you will
        assign the lambda function to that variable
    so that means if you call that variable with an argument
    that argument will be the value of x
    and then the function already has the value of n from when it was made
    so test = lambda x: x * n
    where we said n is 5
    then i do test(3)
    i get 15
    """


def pipeline(*funcs: Callable) -> Callable:
    """Return a single function that applies each func in sequence (left to right).

    pipeline(f, g, h)(x) is equivalent to h(g(f(x))).
    If no functions are provided, the returned function is the identity: f(x) == x.

    Examples:
        >>> add1 = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> pipeline(add1, double)(3)
        8
        >>> pipeline()(42)
        42
    """
    def pipeline_helper(a):
        result = a
        for f in funcs:
            result = f(result)
        return result
    return pipeline_helper
    # raise NotImplementedError("Implement pipeline()")
    """
    Ethan's Notes:
    if the call is pipeline(...)(a) then we call helper and pass a and set that to result
    so then if there are no funcs we return that result anyway
    but otherwise we then go through each function in funcs and set result to its output
        when passed result
    """


def memoize(f: Callable) -> Callable:
    """Return a version of f that caches results by argument.

    Calling the memoized function with the same argument a second time
    must return the cached result WITHOUT calling f again.

    Use a closure over a dict to store previously computed results.

    Examples:
        >>> call_count = 0
        >>> def tracked(x):
        ...     global call_count
        ...     call_count += 1
        ...     return x ** 2
        >>> cached = memoize(tracked)
        >>> cached(4)
        16
        >>> cached(4)   # should not increment call_count
        16
    """
    cache = {}

    def memo_helper(*a):
        if a not in cache:
            cache[a] = f(*a)
        return cache[a]

    return memo_helper
    # raise NotImplementedError("Implement memoize()")
    """
    Ethan's Notes:
    basically because when we do cached = memoize(tracked) python needs to keep tracked in memory
    and because that's being run through the inner memo_helper, it also needs to keep cache dict
        in memory
    so it doesn't actually reset the dict when we run it again since it's calling through that inner
        function and not actually the outer one
    """

"""
Ethan's Section 1.4 Higher-order Functions Notes:
    this one was an actual challenge, mostly new implementations of concepts i already knew
    probably worth looking over again at some point
"""
# ── Part 5: Classes ───────────────────────────────────────────────────────────


class Student:
    """A student with a name and a list of grades (0-100).

    Supports comparison via average grade, enabling natural sorting.
    """

    def __init__(self, name: str, grades: list[float]) -> None:
        self.name = name
        self.grades = grades

    def average(self) -> float:
        """Return the mean of all grades. Returns 0.0 if grades is empty."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)
        # raise NotImplementedError("Implement Student.average()")

    def highest(self) -> float:
        """Return the highest grade. Returns 0.0 if grades is empty."""
        if not self.grades:
            return 0.0
        return max(self.grades)
        # raise NotImplementedError("Implement Student.highest()")

    def letter_grade(self) -> str:
        """Return the letter grade for this student's average.

        Boundaries: A >= 90, B >= 80, C >= 70, D >= 60, F otherwise.
        """
        gpa = self.average()
        if gpa >= 90:
            return "A"
        elif gpa >= 80:
            return "B"
        elif gpa >= 70:
            return "C"
        elif gpa >= 60:
            return "D"
        else:
            return "F"
        # elif check_if_ramaz_student(self):
            # return "Inflated grades: 10000000"
        # raise NotImplementedError("Implement Student.letter_grade()")

    def __repr__(self) -> str:
        """Return a string like: Student('Alice', avg=88.5)"""
        return f"Student('{self.name}', avg={self.average()})"
        # raise NotImplementedError("Implement Student.__repr__()")

    def __lt__(self, other: "Student") -> bool:
        """Compare students by average grade (enables sorted() and min/max)."""
        return self.average() < other.average()
        # raise NotImplementedError("Implement Student.__lt__()")


class Gradebook:
    """Manages a collection of students, keyed by name."""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        """Add a student to the gradebook.

        Raises ValueError if a student with the same name already exists.
        """
        if student.name in self.students:
            raise ValueError
        self.students[student.name] = student
        # raise NotImplementedError("Implement Gradebook.add_student()")

    def top_students(self, n: int) -> list[Student]:
        """Return the n students with the highest averages, in descending order."""
        leaderboard = sorted(self.students.items(), key = lambda item: item[1], reverse=True)
        return [leaderboard[i][1] for i in range(n)]
        # raise NotImplementedError("Implement Gradebook.top_students()")

    def class_average(self) -> float:
        """Return the mean of all student averages. Returns 0.0 if empty."""
        if not self.students:
            return 0.0
        all_gpas = [gpa for avg in self.students.values() for gpa in avg.grades]
        return sum(all_gpas) / len(all_gpas)
        # raise NotImplementedError("Implement Gradebook.class_average()")