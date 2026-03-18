## 混合排序演算法的實證觀察：基於 Python 的 RunMerge Sort 效能分析
 Empirical Observation of Hybrid Sorting Algorithm: Performance Analysis of RunMerge Sort Based on Python

## 題目目標
建立一個自訂排序演算法，並分析其時間複雜度。

## 我設計的演算法：RunMerge Sort
RunMerge Sort 是一個混合式排序法，核心設計如下：
1. 掃描陣列並找出自然有序區段（run）。
2. 若 run 太短，使用 Binary Insertion Sort 補強到 `min_run` 長度。
3. 以 Bottom-up Merge 的方式，將所有 run 逐層合併。

這個做法的目標是利用「資料常常不是完全亂序」的特性，讓接近有序的資料在實務上更快。

## 演算法流程（高階）
1. `detect_runs(A)`：
   - 連續遞增視為一個 run。
   - 若遇到遞減 run，先反轉成遞增。
2. `boost_small_runs(A, runs, min_run)`：
   - 對過短 run 做 Binary Insertion Sort。
3. `merge_all_runs(A, runs)`：
   - 重複兩兩合併 run，直到只剩一個完整 run。

## 時間複雜度分析
令輸入大小為 $n$。

### 1) Detect Runs
- 只需線性掃描一次陣列。
- 時間：$O(n)$。

### 2) Boost Small Runs（Binary Insertion）
- 對每個 run 做 Binary Insertion Sort 以補強到 `min_run`。
- 若 `min_run` 視為常數（本程式預設 32），此步驟總成本可視為 $O(n)$。
- 直觀上是「很多個小區段排序」，而不是對整個長陣列做插入排序。

### 3) Merge All Runs
- 每層合併總成本約 $O(n)$。
- 層數約 $\\log n$。
- 總計 $O(n \\log n)$。

### 綜合複雜度
- 最佳情況（資料已接近有序，run 很長）：$O(n)$ 到 $O(n \\log n)$ 間，通常偏近 $O(n)$。
- 平均情況：$O(n \\log n)$。
- 最壞情況：$O(n \\log n)$（在此設計下，merge 主導；run 補強成本受固定 `min_run` 限制）。

### 空間複雜度
- 合併時需要暫存左右子陣列。
- 空間：$O(n)$。

## 與文獻/經典方法的關聯
本演算法參考了以下設計思想：
1. **Natural Merge Sort**：先利用天然有序片段（run）再合併。
2. **Insertion Sort + Binary Search**：在小片段排序時提升效率。
3. **Hybrid Sorting（如 Timsort 的精神）**：將 run 偵測、插入排序、合併排序組合。

## 程式檔案
- `runmerge_sort.py`

可直接執行：
```bash
python runmerge_sort.py
```

輸出會顯示：
- 不同資料分布（sorted/reversed/random）的執行時間
- 比較次數與搬移次數
- 最終是否排序正確

## 實測結果（2026-03-18）
使用 `n=2000` 的三種資料分布測試：

| Dataset | Time (s) | Comparisons | Moves | Sorted |
|---|---:|---:|---:|---|
| sorted | 0.002488 | 19964 | 1999 | True |
| reversed | 0.002530 | 19964 | 3999 | True |
| random | 0.005208 | 22160 | 30208 | True |

說明：三組資料皆成功排序（`sorted=True`），代表演算法實作正確。

## 可放進報告的結論
RunMerge Sort 在理論上保有 merge-based 的 $O(n \\log n)$ 平均與最壞時間，且利用 run 偵測在近乎有序資料上取得更好的實務效能；其代價是需要 $O(n)$ 額外空間來進行合併。