from pylab import *  # alternatively import numpy and matplotlib

# load the data
def load_data():
    # load data
    data = matrix(genfromtxt('unbalanced_2class.csv', delimiter=','))
    x = asarray(data[:,0:2])
    y = asarray(data[:,2])
    y.shape = (size(y),1)
    return x,y

# run newton's method
def newtons_method(x,y):
    # make full data matrix and initialize weights
    temp = shape(x)
    temp = ones((temp[0],1))
    X = concatenate((temp,x),1)
    X = X.T
    w = randn(3,1)

    # # create container for objective value path - useful for debugging
    # obj_path = []
    # obj = calculate_obj(X,y,w)
    # obj_path.append(obj)

    # pre-compute some quantities to avoid redundant computations
    H = dot(diag(y[:,0]),X.T)
    s = shape(y)
    s = s[0]
    l = ones((s,1))

    # begin newton's method loop
    k = 1
    max_its = 20   # with Newton's method you'll never need more than 100 iterations, and 20 is more than enough for this example
    while k <= max_its:
        # compute gradient
        temp = 1/(1 + my_exp(dot(H,w)))
        grad = - dot(H.T,temp)

        # compute Hessian
        g = temp*(l - temp)
        hess = dot(dot(X,diag(g[:,0])),X.T)

        # take Newton step = solve Newton system
        temp = dot(hess,w) - grad
        w = dot(linalg.pinv(hess),temp)
        # w = linalg.solve(hess, dot(hess,w) - grad)    # much faster, but need to regularize Hessian in order to avoid numerical problems

        # update counter
        k+=1

        # # update path containers - useful for debugging
        # obj = calculate_obj(X,y,w)
        # obj_path.append(obj)
        # iter+= 1
    # # uncomment for use in testing if algorithm minimizing/converging properly
    # obj_path = asarray(obj_path)
    # obj_path.shape = (iter,1)
    # plot(asarray(obj_path))
    # show()

    return w

# calculate the objective value for a given input weight w
def calculate_obj(X,y,w):
    obj = log(1 + my_exp(-y*dot(X.T,w)))
    obj = obj.sum()
    return obj

# avoid overflow when using exp - just cutoff after arguments get too large/small
def my_exp(u):
    s = argwhere(u > 100)
    t = argwhere(u < -100)
    u[s] = 0
    u[t] = 0
    u = exp(u)
    u[t] = 1
    return u

# plotting function
def plot_fit(x,y,w):
    # initialize figure, plot data, and dress up panels with axes labels etc.,
    fig = plt.figure(facecolor = 'white')
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('$x_1$',fontsize=20,labelpad = 20)
    ax1.set_ylabel('$x_2$',fontsize=20,rotation = 0,labelpad = 20)
    s = argwhere(y == 1)
    s = s[:,0]
    scatter(x[s,0],x[s,1], s = 30,color = (1, 0, 0.4))
    s = argwhere(y == -1)
    s = s[:,0]
    scatter(x[s,0],x[s,1],s = 30, color = (0, 0.4, 1))
    ax1.set_xlim(min(x[:,0])-0.1, max(x[:,0])+0.1)
    ax1.set_ylim(min(x[:,1])-0.1,max(x[:,1])+0.1)

    # plot separator
    r = linspace(0,1,150)
    z = -w.item(0)/w.item(2) - w.item(1)/w.item(2)*r
    ax1.plot(r,z,'-k',linewidth = 2)
    show()

##### main #####
def main():
    # load data
    x,y = load_data()

    # run newtons method to minimize logistic regression or softmax cost
    w = newtons_method(x,y)

    # plot everything - including data and separator
    plot_fit(x,y,w)

main()