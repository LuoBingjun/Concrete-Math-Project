/**
 * COPYRIGHT NOTICE
 * Copyright (c) 2014, Institute of CG & CAD, Tsinghua University.
 * All Rights Reserved.
 * 
 * @file    main.cpp
 * @brief   Write your own code here.
 * 
 * @version 1.1
 * @author  Jackie Pang
 * @e-mail: 15pengyi@gmail.com
 * @date    2012/10/11
 * @reviser	Gong Chao
 * @date	2014/10/13
 * @e-mail:	gcdofree@gmail.com
 * @reviser	Zhang Mingdong
 * @date	2017/10/10
 * @e-mail:	zhangmd14@mails.tsinghua.edu.cn
 */

#include <iostream>
#include <vector>
#include "USSolver.h"
bool *flag;
int *A;
int *B;
int v, e;

void dfs(int des, int now, std::vector<int> path, std::ostream &outputStream)
{
	if (now == des && path.size() >= 2)
	{
		outputStream << "[";
		for (int i = 0; i < path.size(); i++)
		{
			if (i != path.size() - 1)
				outputStream << path[i] << " -> ";
			else
				outputStream << path[i] << "]";
		}
		return;
	}
	for (int i = A[now]; i < A[now + 1]; i++)
	{
		if (!flag[B[i]])
		{
			flag[B[i]] = 1;
			std::vector<int> temp = path;
			temp.push_back(B[i]);
			dfs(des, B[i], temp, outputStream);
			flag[B[i]] = 0;
		}
	}
}

void USSolver::Solve(std::istream &inputStream, std::ostream &outputStream)
{
	//请在此填充代码
	inputStream >> v >> e;
	A = new int[v + 1];
	B = new int[e];
	for (int i = 0; i <= v; i++)
		inputStream >> A[i];
	for (int i = 0; i < e; i++)
		inputStream >> B[i];
	int **M = new int *[v];
	for (int i = 0; i < v; i++)
	{
		M[i] = (int *)malloc(v * sizeof(int));
		memset(M[i], 0, v * sizeof(int));
	}
	for (int i = 0; i < v; i++)
		for (int j = A[i]; j <= A[i + 1] - 1; j++)
		{
			M[i][B[j]] = 1;
		}
	for (int k = 0; k < v; k++)
		for (int i = 0; i < v; i++)
			for (int j = 0; j < v; j++)
				M[i][j] = M[i][j] || (M[i][k] && M[k][j]);
	int n;
	inputStream >> n;
	for (int i = 1; i <= n; i++)
	{
		int vs, ve;
		inputStream >> vs >> ve;
		if (M[vs][ve] == 0)
		{
			outputStream << "NO PATH" << std::endl;
		}
		else
		{
			flag = new bool[v];
			memset(flag, 0, v * sizeof(bool));
			std::vector<int> path;
			path.push_back(vs);
			flag[vs] = 1;
			flag[ve] = 0;
			dfs(ve, vs, path, outputStream);
			outputStream << std::endl;
		}
	}
}



int main(int argc, char *argv[])
{
	//可在此更改测试文件
    std::string fileName = "test101.txt"; 
    
    USSolver unofficialSolver(fileName);
    const std::string unofficialAnswer = unofficialSolver.GetAnswer();

    std::cout << "Your Answer:" << unofficialAnswer << std::endl;
}