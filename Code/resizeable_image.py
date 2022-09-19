# Andrew Fang and Hari Patchigolla

import imagematrix
import time

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        start = time.time()     # keep tracks of how long the algorithm takes
        coords = []             # list of coordinates for pixels in best seam
        if dp:                  # using dynamic programming
            DP = [[0 for x in range(self.height)] for y in range(self.width)]   # DP table to calculate subproblems
            # lines 10-20 : populating the DP table
            for j in range(self.height):        # fills in DP table row by row
                for i in range(self.width):     # iterates across each row
                    if j == 0:                  # BASE CASE : checks if it is the first row of the DP table and sets it to their respective energy value
                        DP[i][j] = self.energy(i,j)
                    elif i - 1 < 0:             # checks if the current pixel is on the rightmost edge
                        DP[i][j] = min(DP[i][j-1], DP[i+1][j-1]) + self.energy(i,j)
                    elif i + 1 > self.width - 1:# checks if the current pixel is on the leftmost edge
                        DP[i][j] = min(DP[i-1][j-1], DP[i][j-1]) + self.energy(i,j)
                    else:                       # checks if the current pixel is on the leftmost edge
                        DP[i][j] = min(DP[i-1][j-1], DP[i][j-1], DP[i+1][j-1]) + self.energy(i,j)
            # lines 22-25 : finds the seam with the minimum energy value by iterating across the last row 
            minx = 0    # x value of best seam
            for i in range(self.width):
                if DP[i][self.height-1] < DP[minx][self.height-1]:      # saves x value of smallest energy seam
                    minx = i
            # back tracking from the minimum energy value to find the coordinates of the best seam
            curx = minx                         # starts at the bottom of the best seam
            cury = self.height-1
            # while the current y value doesn't equal the topmost row, continue computing the best seam
            while(cury >= 0):
                coords.append((curx,cury))      # adds the current pixel to coords
                cury -= 1                       # following finds which of the three pixels above has the smallest energy and sets next value to that
                smallest = min(DP[curx-1][cury], DP[curx][cury], DP[curx+1][cury]) 
                if smallest == DP[curx-1][cury]:
                    curx -= 1
                elif smallest == DP[curx+1][cury]:
                    curx += 1
            print(time.time() - start)          # how long it takes to run DP
        else:                                   # not using dynammic programming
            minenergy = (0, self.subproblem(0,self.height-1))   # saves x value and energy value of best seam
            for i in range(self.width):
                cur = self.subproblem(i,self.height-1)
                if cur < minenergy[1]:          # if the current computed seam energy is smaller than the current min
                    minenergy = (i, cur)        # update x value and energy value of the best seam
            
            curx = minenergy[0]                 # starting x value
            cury = self.height-1                # starting y value

            while (cury >= 0):
                coords.append((curx,cury))      # adds current pixel to coords
                if cury == 0:                   # break out of loop in cury is zero
                    break
                a = self.subproblem(curx-1, cury-1)
                b = self.subproblem(curx, cury-1)
                c = self.subproblem(curx+1, cury-1)
                smallest = min(a,b,c)           # finds which of the three pixels above has the smallest energy and sets next value to that
                if smallest == a:
                    curx -= 1
                if smallest == c:
                    curx += 1
                cury -= 1

            print(time.time() - start)      # how long it takes to run non DP
        
        return coords                       # returns the coordinates for the pixels of the best seam
    
    def subproblem(self, i, j):             # uses recursion to solve for the best seam
        if j > 0:
            if i - 1 < 0:               # checks if the current pixel is on the rightmost edge
                return min(self.subproblem(i,j-1), self.subproblem(i+1,j-1)) + self.energy(i,j)
            elif i + 1 > self.width-1:  # checks if the current pixel is on the leftmost edge
                return min(self.subproblem(i-1,j-1), self.subproblem(i,j-1)) + self.energy(i,j)
            else:                       # checks if the current pixel is on the leftmost edge
                return min(self.subproblem(i-1,j-1), self.subproblem(i,j-1), self.subproblem(i+1,j-1)) + self.energy(i,j)
        else:                           # BASE CASE : checks if it is the first row of the DP table and sets it to their respective energy value
            return self.energy(i,j)