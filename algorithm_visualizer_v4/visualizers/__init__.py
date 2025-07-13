from visualizers.BubbleSortViz import BubbleSortViz
from visualizers.InsertionSortViz import InsertionSortViz
from visualizers.SelectionSortViz import SelectionSortViz
from visualizers.MergeSortViz import MergeSortViz
from visualizers.QuickSortViz import QuickSortViz
from visualizers.CountingSortViz import CountingSortViz
from visualizers.BFSTreeViz import BFSTreeViz
from visualizers.DFSTreeViz import DFSTreeViz
from visualizers.BinarySearchViz import BinarySearchViz

VIZ_REGISTRY = {
    "Bubble Sort"   : BubbleSortViz,
    "Insertion Sort": InsertionSortViz,
    "Selection Sort": SelectionSortViz,
    "Merge Sort"    : MergeSortViz,
    "Quick Sort"    : QuickSortViz,
    "Counting Sort" : CountingSortViz,
    "BFS (Tree)"    : BFSTreeViz,
    "DFS (Tree)"    : DFSTreeViz,
    "Binary Search" : BinarySearchViz,
}
