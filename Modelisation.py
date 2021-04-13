
@api_view(['POST'])
def ViewChart(request):
    files = glob.glob('/chart/*')
    for f in files:
        os.remove(f)
    data = json.loads(request.body)
    graphDetails = data['details']


    print(graphDetails)
    # Set data
    df = pd.DataFrame(graphDetails)
    
    # number of variable
    categories=list(df)[1:]
    N = len(categories)
    
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=df.loc[0].drop('AAgroup').values.flatten().tolist()
    values += values[:1]
    values
    
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([25,50,75], ["25","50","75"], color="grey", size=7)
    plt.ylim(0,100)
    
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    ax.legend(loc='upper left', frameon=False)

    num = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(" ", "")

    plt.savefig('/var/www/html/bulmav2/thotea/chart/radar'+ num+'.png')

    plt.close()

    results ={
        'result':num
    }
    return JsonResponse(results)
