
        function t = fuse(Flatten,FC6,FC7,labels)
            [Ax1,Ay1,Xs1,Ys1] = dcaFuse(Flatten,FC6,labels);
            [Ax2,Ay2,Xs2,Ys2] = dcaFuse(FC7,FC6,labels);
            level2_X = Xs1 + Ys1;
            level2_Y = Xs2 + Ys2;

            [Ax_out,Ay_out,Xs_out,Ys_out] = dcaFuse(level2_X,level2_Y,labels);

            final_output = Xs_out + Ys_out;
            t = final_output';
            
            end
        