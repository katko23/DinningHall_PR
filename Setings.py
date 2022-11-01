#order :
#
hostName = "localhost"
serverPort = 27003

serverName =  "localhost"
this_serverPort = 27004

FoodOrderingService_Host = "localhost"
FoodOrderingService_Port = 27001

# hostName = "kitchen-c"
# serverPort = 27003
#
# serverName =  "dinning-c"
# this_serverPort = 27004
#
# FoodOrderingService_Host = "foodorderingservice-c"
# FoodOrderingService_Port = 27001

nr_of_tables = 6
nr_of_waiters = 3
timeunit = 0.1
restaurant_id = 1
nr_of_chef_cooks = 1
nr_of_line_cooks = 2
nr_of_saucier = 1
nr_of_ovens = 2
nr_of_stoves = 1
wt = 42/(nr_of_chef_cooks * 3 + nr_of_line_cooks * 1 + nr_of_saucier * 2) + 62/(nr_of_ovens + nr_of_stoves)
