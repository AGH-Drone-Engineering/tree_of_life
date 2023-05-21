#include<bits/stdc++.h>
 
using namespace std;
constexpr int V = 30; 
constexpr int INF = 21376969;
float g[V][V];
bool completed[V];
int n;
float fullDist;
vector<int> wyniki;
 
int least(int v){
	int nc=INF;
	int min=INF;
	int kmin;
	for(int i=0; i<n; i++){
		if(g[v][i] && !completed[i])
		if(g[v][i]*2 < min){
			min=g[i][0]+g[v][i];
			kmin=g[v][i];
			nc=i;
		}
	}
	if(min!=INF)	fullDist+=kmin;
	return nc;
}
 
void minimalnyKoszt(int v){
	completed[v] = true;
	wyniki.push_back(v+1);
	int nv=least(v);
	if(nv==INF){
		nv=0;
		wyniki.push_back(nv+1);
		fullDist += g[v][nv];
	}
	else minimalnyKoszt(nv);
}
 
int main(){
	cin>>n;
	pair<float, float> wierz[V+5];
	for(int i=0; i<n; i++)	cin>>wierz[i].first>>wierz[i].second;
	for(int i=0; i<n; i++){
		for(int j=0; j<=n; j++){
			if(i==j) continue;
			float odl = sqrt(pow(wierz[i].first-wierz[j].first, 2) + pow(wierz[i].second-wierz[j].second, 2)); 
			g[i][j] = odl;
		}
	}
	minimalnyKoszt(0);
	for(auto i:wyniki) cout<<i<<" ";
	cout<<endl<<"------------------------------------------------------"<<endl;
	cout<<"Najkrótsza ścieżka to: "<<fullDist;
	return 0;
}