

## Pruning with Eigenvalue

考虑对特征值进行更新，如果在更新的过程中可以找到特征值的界，则可以利用上界和下界与Cauthy交错定理进行剪枝，



如果$C$是$A$的 $n-k$ 阶主子阵，


$$
\lambda_i(A) \le \lambda_i(C) \le \lambda_{i+k}(A)
$$


如果找到了$\lambda(A)$的界$\mu(A)$， 我们有，


$$
m_i(A) \le \lambda_i(A) \le \lambda_i(C) \le \lambda_{i+k} (A) \le M_{i+k}(A)
$$


也即如果满足Induced SupGraph的要求，可以得到下式一定需要满足，


$$
\lambda_i(C) \in [m_i(A), M_{i+k}(A)]
$$


## Static Initialization

计算出特征值之后，$\mu_i(A) = \lambda_i(A)$, 根据矩阵分析定理8.2.9，

根据樊畿定理，可以给出关于特征值的圆盘估计，
$$
\begin{align}
\cup_{i=1}^N R(a_{ii},\rho(B) -1)
\end{align}
$$


## Dynamic Update

本节证明在动态更新的时候，特征值的该变量是很小的。

只考虑加边和加点的情况，对于减边和减点的情况类似。

简单的是加点的情况，矩阵新增一个维度，增加一个零特征值为最小特征值。

下面考虑加边的情况，可以归结为对一个邻接矩阵$A$, 施加了一个低秩扰动 $B$,

可以计算得到矩阵$B$的特征值满足，


$$
\begin{align}
\det(B) &= \lambda^{n-2}(\lambda^2-1) \\
\lambda_{1}(B) &= -1, \lambda_n(B) = 1, \lambda_{1<j<n}(B) = 0 
\end{align}
$$


根据Hoffman–Wielandt不等式和Young定理等，我们知道更新操作对特征值的改动是很小的，


$$
\begin{align}
\sum_{i=1}^N (\lambda_i(A+B) - \lambda_i(A))^2 &\le \Vert B \Vert_F^2 =4 \\
\max_i \lambda_i(A+B) - \lambda_i(A) &\le \Vert B \Vert_2 = 1
\end{align}
$$


每次更新的界可以根据Weyl不等式得到，


$$
\lambda_{i-j+1}(A) + \lambda_j(B) \le \lambda_i(A+B) \le \lambda_{i+j}(A) + \lambda_{n-j}(B)
$$


枚举最优的$j$可以得到界，


$$
\begin{align}
m_i(A+B) &= \max_j  \lambda_{i-j+1}(A) + \lambda_j(B) \\
&= \max[\lambda_i(A) -1, \lambda_{i-n+1}+1,\lambda_{i-j+1,1<j<n}(A)] \\
M_i(A+B) &= \min_j \lambda_{i+j}(A) + \lambda_{n-j}(B) \\
&= \min [\lambda_{i+n-1}(A)-1,\lambda_i(A)+1, \lambda_{i-j+1,1<j<n}(A)]
\end{align}
$$



最终得到，
$$
m_i(A+B) \le \lambda_i(A+B) \le M_i(A+B)
$$







