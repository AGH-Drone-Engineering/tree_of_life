#include <bits/stdc++.h>
using namespace std;
constexpr int M = 50;
vector<vector<pair<int, float>>> g(M);
float fullDist;
vector<pair<int, int>> wziete;
bool odw[M];
void dfs(int v){
	pair<int, float> wybrany = {0, 200000};
	odw[v] = 1;
	for(auto i:g[v])if(!odw[i.first]){
		if(wybrany.second > i.second){
			wybrany.first = i.first;
			wybrany.second = i.second;
		}
	}
	
	if(wybrany.first==0 && wybrany.second==200000) return;
	else{
		fullDist+=wybrany.second;
		dfs(wybrany.first);
		wziete.push_back({v, wybrany.first});
	}
}

int main(){
	
	int n;
	cin>>n;
	pair<int, int> wierz[n+5];
	for(int i=1; i<=n; i++){
		cin>>wierz[i].first>>wierz[i].second;
	}
	for(int i=1; i<=n; i++){
		for(int j=1; j<=n; j++){
			if(i==j) continue;
			float odl = sqrt(pow(wierz[i].first-wierz[j].first, 2) + pow(wierz[i].second-wierz[j].second, 2)); 
			g[i].push_back({j, odl});
		}
	}
	dfs(1);
	for(int i=1; i<=n; i++){
		cout<<i<<": ";
		for(auto j:g[i]) cout<<j.first<<", "<<j.second<<"    ";
		cout<<endl;
	}
	cout<<"--------------------------------------"<<endl;
	cout<<"nasz trasa: "<<endl;
	reverse(wziete.begin(), wziete.end());
	for(auto i:wziete) cout<<i.first<<"->"<<i.second<<endl;
	cout<<"--------------------------------------"<<endl;
	cout<<"nasza cała trasa ma: "<<fullDist<<" metrów"<<endl;
	
	return 0;
}