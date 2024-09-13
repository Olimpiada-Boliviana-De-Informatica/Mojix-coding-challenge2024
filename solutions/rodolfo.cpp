#include <iostream>
#include <vector>

using namespace std;

int disc_by_column[140];
int board[120][140];
int q_disc_win = 4;
int rows,cols;
bool winner = false;
int mc,g,k; // mc is my color, g is game type, k is the column that opponent moves
int oc; // od is the opponent's color
int rc[8]={-1,-1,0,1,1,1,0,-1};
int cc[8]={0,1,1,1,0,-1,-1,-1};
vector<bool>bad_column;
int has_win(){
	// returns the color of the player that has win or -1 if nobody has win yet
	for(int i=0;i<rows;i++){
		for(int j=0;j<cols;j++){
			if(board[i][j]!=0){
				for(int k=0;k<8;k++){
					// Check if there is a winner in certain direction
					bool win_direction=true;
					int r=i;
					int c=j;
					for(int q=1;q<q_disc_win;q++){
						r+=rc[k];
						c+=cc[k];
						if(r>=0 && r<rows && c>=0 && c<cols && board[i][j]==board[r][c]){
							continue;
						}
						else{
							win_direction=false;
							break;
						}
					}
					if(win_direction){
						return board[i][j];
					}
				}
			}
		}
	}
	return -1;
}

pair<int,int> can_win(){ 
	// checks if a participant  can win
	// return a pair <int,int>
	// first component is -1 if the player with color c, can't win
	// otherwise first component is kc, that represent the column that player with
	// color c has to move in order to win
	// second component is -1 if the player with color oc, can't win
	// otherwise first component is kc, that represent the column that player with
	// color oc has to move in order to win
	int col_to_win_mc = -1, col_to_win_oc = -1;
	for(int i=0;i<rows;i++){
		for(int j=0;j<cols;j++){
			if(board[i][j]!=0){
				for(int k=0;k<8;k++){
					// Check if connect in certain direction
					bool win_direction=true;
					int r=i;
					int c=j;
					int qfilled=1;
					int qfree=0;
					int cfree=-1;
					int rfree=-1;
					for(int q=1;q<q_disc_win;q++){
						r+=rc[k];
						c+=cc[k];
						if(r>=0 && r<rows && c>=0 && c<cols){
							if(board[i][j]==board[r][c]){
								qfilled++;
							}
							else{
								if(board[r][c]==0){
									qfree++;
									cfree=c;
									rfree=r;
								}
								else{
									win_direction=false;
								}
							}
							
						}
						else{
							win_direction=false;
							break;
						}
					}
					if(win_direction){
						// This means that probably only one disc remains for win
						if(qfree==1){
							if(rfree>=1 && board[rfree-1][cfree]!=0){
								// In one movement the game could end
								if(board[i][j]==mc){
									col_to_win_mc = cfree;
								}
								else{
									col_to_win_oc = cfree;
								}
							}
							else{
								// For bad columns that a move in there will make the opponent win in the next step
								if(rfree>=2 && board[rfree-2][cfree]!=0){
									bad_column[cfree]=true;
								}
							}
						}
					}
				}
			}
		}
	}
	return make_pair(col_to_win_mc,col_to_win_oc);
}

int calculate_heu(int i,int j){
	// Heuristic most directions that can led to a win
	if(bad_column[j]) return -2;
	int h=0;
	for(int k=0;k<8;k++){
		int qfilled=0;
		int qfree=0;
		int r=i;
		int c=j;
		bool win_direction=true;
		for(int q=1;q<q_disc_win;q++){
			r+=rc[k];
			c+=cc[k];
			if(r>=0 && r<rows && c>=0 && c<cols){
				if(board[i][j]==board[r][c]){
					qfilled++;
				}
				else{
					if(board[r][c]!=0){
						win_direction=false;
						break;
					}
				}
			}
			else{
				win_direction=false;
				break;
			}
		}
		if(win_direction){
			h+=qfilled;
		}
	}
	return h;
}

int calculate_column(){
	int choosen=-1;
	int max_heu=-1;
	int l=0, r=cols-1;
	while(l<=r){
		int c_heu=calculate_heu(disc_by_column[l],l);
		if(c_heu>=max_heu){
			choosen=l;
			max_heu=c_heu;
		}
		c_heu=calculate_heu(disc_by_column[r],r);
		if(c_heu>=max_heu){
			choosen=r;
			max_heu=c_heu;
		}
		l++;
		r--;
	}
	return choosen;
}

int calculate_column_2(){
	/// We have to preffer horizontal
	int choosen=-1;
	int max_heu=-1;
	for(int i=0;i<cols;i++){
		int c_heu=calculate_heu(disc_by_column[i],i);
		if(c_heu>=max_heu){
			choosen=i;
			max_heu=c_heu;
		}
	}
	return choosen;
}

bool board_full(){
	for(int i=0;i<rows;i++){
		for(int j=0;j<cols;j++){
			if(board[i][j]==0) return false;
		}
	}
	return true;
}

int main(){
	cin>>mc>>g;
	if(g==1){
		rows=6;
		cols=7;
	}
	else if(g==2){
		rows=100;
		cols=7;
	}
	else if(g==3){
		rows=10;
		cols=70;
	}
	else{
		rows=120;
		cols=140;
		q_disc_win=5;
	}
	// Initialize board and disc_by_column
	for(int i=0;i<rows;i++)
		for(int j=0;j<cols;j++){
			board[i][j]=0;
			disc_by_column[j]=0;
		}
	if(mc==1){
		// I started
		// Always chose the row at middle
		cout<<(cols/2)+1<<"\n"; // Add 1 because the answer is in a 1-based board
		board[0][cols/2]=mc;
		disc_by_column[(cols/2)]++;
		oc=2;
	}
	else{
		oc=1;
	}
	while(!winner){
		// RE START BAD COLUMN
		if(board_full()){
			//cout<<"TIE\n";
			break;
		}
		bad_column.clear();
		bad_column.assign(cols,false);
		// START OPPONENT MOVE
		cin>>k;
		k--; // I am working in 0-based board
		if(disc_by_column[k]>=rows){
			// This is not supposed to pass but just to be sure
			// cout<<"THE OPPONENT HAS PUT A DISK OUTSIDE THE BOARD\n";
		}
		board[disc_by_column[k]][k]=oc;
		disc_by_column[k]++;
		// Check if with the last opponents move, there is a winner
		if(has_win()==oc){
			winner=true;
			//cout<<"I LOSE\n";
			// OPPONENT HAS WIN, my program not print anything more
			continue;
		}
		// FINISH OPPONENT MOVE

		// START MY MOVEMENT
		// Check if some player can win
		// cout<<"BOARD TO BE ANALIZED FOR MAKE MY MOVEMENT"<<endl;
		/*for(int i=0;i<rows;i++){
			for(int j=0;j<cols;j++){
				cout<<board[i][j]<<" ";
			}
			cout<<endl;
		}
		cout<<"Q DISC"<<endl;
		for(int i=0;i<cols;i++){
			cout<<disc_by_column[i]<<" ";
		}
		cout<<endl<<"-------------------"<<endl;*/
		int column_chossen = -1;
		pair<int,int> ans = can_win();
		/*cout<<"RETURN OF CAN WIN"<<endl;
		cout<<ans.first<<" "<<ans.second<<endl;*/
		if(ans.first!=-1){ // I can win
			// So I will win
			column_chossen = ans.first;
		}
		else if(ans.second!=-1){ // I can lose
			// So I will block that movement
			column_chossen = ans.second;
		}
		else{
			// If I cant win nor lose
			if(g==1 or g==2){
				column_chossen = calculate_column();
			}
			else{
				column_chossen = calculate_column_2();
			}
		}
		// CHECK IF IS A BAD CHOOSSEN if that select the first available col by left
		int first_available_column=0;
		int first_not_bad_column=-1;
		bool is_first=true;
		if(column_chossen<0 || column_chossen>=cols || disc_by_column[column_chossen]==rows){
			for(int i=0;i<cols;i++){
				if(disc_by_column[i]<rows){
					if(is_first){
						first_available_column=i;
						is_first=false;
					}
					if(!bad_column[i]) first_not_bad_column=i;
				}
			}
			if(first_not_bad_column!=-1) column_chossen=first_not_bad_column;
			else column_chossen=first_available_column;
		}
		// UPDATE BOARD
		board[disc_by_column[column_chossen]][column_chossen]=mc;
		disc_by_column[column_chossen]++;
		// PRINT MY MOVEMENT
		cout<<column_chossen+1<<"\n";
		// Check if with my move I won
		if(has_win()==mc){
			winner=true;
			//cout<<"I WIN\n";
			// I WIN, the program not print anything more
			continue;
		}
	}
	return 0;
}
