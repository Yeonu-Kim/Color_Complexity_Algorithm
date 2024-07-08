# Color_Complexity_Algorithm

> Calculate Color Complexity Using Cross Entropy

---

## Reference

Zhou, B., Xu, S., & Yang, X. X. (2015, August). Computing the color complexity of images. In 2015 12th International Conference on Fuzzy Systems and Knowledge Discovery (FSKD) (pp. 1898-1902). IEEE.

https://scholar.google.co.kr/scholar?hl=ko&as_sdt=0%2C5&q=Computing+the+Color+Complexity+of+Images&btnG=&oq=Colo#d=gs_cit&t=1713940996326&u=%2Fscholar%3Fq%3Dinfo%3ATbfNSebLG5AJ%3Ascholar.google.com%2F%26output%3Dcite%26scirp%3D0%26hl%3Dko


## Method
### 1. Complexity of the Color Variety Feature $(C_s)$

$$
C_s = -\sum\limits_{i=1}^m n_i \, log(\frac{n_i}{N})
$$

$n_i$: The number of pixel which has ith color (i번째 색깔을 가진 픽셀 개수)

m: Total number of unique colors (서로 다른 색깔의 개수)

N: Total number of pixels(전체 픽셀 수)

---


### 2. Complexity of the Color Spatial Distribution Feature ($C_k$)

Area complexity of kth color (k번째 색에 대한 영역 복잡도)

$$
C_k = -\sum\limits_{i=1}^p n_i \, log(\frac{n_i}{N})
$$

$n_i$: The number of pixel in ith area (i번째 영역의 픽셀 개수)

p: Total number of unique area (서로 다른 영역의 개수)

N: Total number of pixels (전체 픽셀 개수)  

---

### 3. Complexity of the total Area

$$
C_d = -\sum\limits_{k=1}^m \frac{C_kn_k}{N}
$$

$n_k$: Total number of pixel in kth color (k번째 색의 픽셀 개수)  
