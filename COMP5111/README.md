# 5511_a1 Project — Vehicle Routing Problem Optimization with DEAP

## ⚙️ Runtime Environment

- **Python version:** 3.10 recommended  
- **Operating System:** Linux / macOS / Windows  
- **Execution:** Jupyter Notebook or **Google colab**

Example environment setup:
- if use Google colab only do that 
```!pip install deap```

## 📦 Required Packages

This project depends on the following Python packages :

```
collections
deap
math
matplotlib
numpy
os
pandas
pickle
random
sklearn
```
Install all dependencies with:

```bash
pip install -r requirements.txt
```




## 📁 Project Structure

```
5511_a1 (2).ipynb     # Main Jupyter Notebook containing code and analysis
README.md             # This README file
requirements.txt      # Dependency list
```

## 📊 Example Usage Snippet

Below is an example of how some core functions might be used in this notebook:

- ```eval_vrp_classical``` can be changed  according to the needs of different question\
- ``` cxpb``` and``` mutpb``` changed to different values ​​for optimization
- ```verbose=False``` NOT print detail of the train

```python
from deap import base, creator, tools, algorithms
import numpy as np

# Create DEAP classes
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", np.random.permutation, range(num_customers))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Register genetic operators
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", eval_vrp_classical)

# Run GA
population = toolbox.population(n=100)
algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=2000, verbose=True) #change cxpb and mutpb
```
## 💾 Save result for next train
- save some best route to ```best_solutions.pkl```
- the next train use that way add the result to the initial pop. Speed ​​up training and it can reduce the number of single training iterations and shorten the single training time
```
  try:
    with open("best_solutions.pkl", "rb") as f:
        saved_solutions = pickle.load(f)
    print(f"✅ 读取了 {len(saved_solutions)} 个历史最优解")
    # 用保存的个体初始化种群前 N 个
    initial_pop = [creator.Individual(sol["individual"]) for sol in saved_solutions]
except FileNotFoundError:
    print("⚠️ 未找到历史最优解文件，将随机初始化种群")
    initial_pop = []
``` 

## ⚙ Build_distance_matrix

By establishing a distance matrix, it is convenient to quickly query the distance between any two points in the VRP path calculation, thereby increasing the operation efficiency.
```python
def build_distance_matrix(coords):
    nodes = sorted(coords.keys())
    arr = np.array([coords[k] for k in nodes])
    diff = arr[:,None,:] - arr[None,:,:]
    dist = np.sqrt((diff**2).sum(axis=2))
    node_to_index = {node:i for i,node in enumerate(nodes)}
    return dist, node_to_index

dist_matrix, node_to_index = build_distance_matrix(coords)

```

## 🖼 Visualization

Typical plots generated in this notebook include:
- Evolution of best fitness values across generations.
- Comparison of routes and depot assignments.
- Convergence curves for multi-objective optimization (e.g., Pareto fronts).


# Q2
- Add normal distrubution
  ```python
  def sample_demands(mean_demands):
    sampled = {}
    for k, mu in mean_demands.items():
        if mu <= 0:
            sampled[k] = 0
        else:
            sd = 0.2 * mu
            x = np.random.normal(mu, sd)
            while x <= 0:
                x = np.random.normal(mu, sd)
            sampled[k] = int(round(x))
    return sampled
  ```
- Add Monte Carlo, replace ```toolbox.register("evaluate", mc_evaluate)```
  ```python
  def mc_evaluate(individual):
    total_dists = []
    feasible_count = 0

    for _ in range(MC_SAMPLES):
        sampled = sample_demands(demands)
        dist_val, _, feasible = compute_distance_with_sample(individual, sampled)
        if feasible and dist_val < 1e9:
            feasible_count += 1
        total_dists.append(dist_val)

    avg_dist = np.mean(total_dists)
    feas_rate = feasible_count / MC_SAMPLES
    score = avg_dist + PENALTY * (1 - feas_rate)
    return (score,)
  
- Set ```MC_SAMPLES = 25``` use 25 Monte Carlo sample, t  oo many times will increase training time


  ----
  # Q3 (cluster)
- Use Kmean
```python
K_CLUSTERS = max(5, int(np.sqrt(len(idx_to_cust))))  
customer_coords = np.array([coords[n] for n in idx_to_cust])
```
- Arrange customers in the same cluster consecutively
  ```python
  def repair_region_blocks(individual):
    # individual: list of idx into idx_to_cust
    # produce customer NO sequence
    seq_nos = [idx_to_cust[i] for i in individual]
    seen = set()
    new_seq = []
    for node in seq_nos:
        c = cust_to_cluster[node]
        if c not in seen:
            seen.add(c)
            # append all nodes of this cluster in the order they appear in seq_nos
            cluster_nodes_in_order = [n for n in seq_nos if cust_to_cluster[n]==c]
            new_seq.extend(cluster_nodes_in_order)
    # now convert back to indices
    idx_map = {cust:i for i,cust in enumerate(idx_to_cust)}
    repaired = [idx_map[n] for n in new_seq]
    # replace content
    individual[:] = repaired
    return individual
  ```
- other part are same as Q1

---
# Q4 (MULTI-OBJECTIVE OPTIMIZATION PROBLEM)

- Update evaluator minmum ```f1``` maxmum ```f2```
  ```python
  def eval_vrp_bi(individual):
        total_dist = 0.0
    total_eff_pen = 0.0  # f2: sum(EFFICIENCY_i - d_i)
    load = 0.0
    cur = depot_no
    segments = []
    seg = [depot_no]
    # For tracking cumulative distance inside current segment
    cum_dist = 0.0

    for idx in individual:
        cust = idx_to_cust[idx]
        cust = int(cust)
        demand = demands.get(cust, 0.0)
        # if adding this customer exceeds capacity -> return to depot and start new trip
        if load + demand > CAPACITY:
            # return to depot
            total_dist += dist_matrix[node_to_index[cur], node_to_index[depot_no]]
            # close segment
            seg.append(depot_no)
            segments.append(seg)
            # reset for next trip
            seg = [depot_no]
            cur = depot_no
            load = 0.0
            cum_dist = 0.0

        # travel from cur to cust
        dist = dist_matrix[node_to_index[cur], node_to_index[cust]]
        total_dist += dist
        cum_dist += dist  # cumulative distance from depot along this segment/trip to reach this customer
        # efficiency contribution: EFFICIENCY_i - d_i
        effi = EFFICIENCY.get(cust, 0.0)
        total_eff_pen += (effi - cum_dist)

        # append
        seg.append(cust)
        cur = cust
        load += demand

    # finish last segment: return to depot
    total_dist += dist_matrix[node_to_index[cur], node_to_index[depot_no]]
    seg.append(depot_no)
    segments.append(seg)

    f1 = total_dist
    f2 = total_eff_pen
    return f1, f2, segments

- ```run_nsga2()``` implements a standard NSGA-II (μ+λ selection) using DEAP for two objectives (minimize distance, maximize efficiency). By default, the function generates an offspring equal to the number of children (i.e., λ = μ) and uses a hard-coded objective normalization constant.
- ```for w in [0.25, 0.5, 0.75, 1.0]```Use different w to calculate ```f = w*f1 - (1-w)*f2```

**some result pic**
- ![w=0.25](images/Q4-1-0.25.png)
- ![w=0.5](images/Q4-1-0.5.png)
- ![w=0.75](images/0.75.png)
- ![w=1.0](images/1.0.png)

---
# Q5 (Pickup-and-Delivery)
- Randomly set 30% of custs as pickup points
- Update ```eval_vrp_pickup_delivery(individual)```
  - Determine whether it is a pickup cust based on the next cust NO encountered
- **some result pic**
  - ![Q5-1](images/Q5-1.png)

  - ![Q5-2](images/Q5-2.png)
