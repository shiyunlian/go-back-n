import matplotlib.pyplot as plt
# lost_packets_buffer = [61, 60, 57, 76, 44, 4, 28, 3, 35, 42, 89, 54, 76, 74, 84, 89]
# lost_packets_time_buffer =[35.3, 64.3, 93.1, 148.0, 167.7, 233.8, 258.7, 311.0, 317.5, 318.9, 328.5, 404.1, 408.6, 418.1, 425.9, 426.9]
# # plotting points as a scatter plot
# #plt.scatter(lost_packets_time_buffer, lost_packets_buffer, label= "stars", color= "green", marker= "*", s=30)
# plt.plot(lost_packets_time_buffer, lost_packets_buffer)
# # x-axis label
# plt.xlabel('time in seconds')
# # frequency label
# plt.ylabel('# of packets dropped')
# # plot title
# plt.title('Packets dropped over time')
# # showing legend
# plt.legend()
# # function to show the plot
# plt.show()

#win_size_buffer =[4, 8, 16, 32, 64, 128, 64, 128, 64, 128, 64, 128, 256, 128, 256, 128, 256, 256, 256, 128, 64, 128, 256, 256, 128, 256, 256, 256, 128, 64, 32, 64]
#win_size_time_buffer=[0,0.6, 2.7, 6.5, 13.5, 22.2, 43.0, 51.4, 72.2, 80.9, 101.7, 110.9, 131.8, 152.7, 158.0, 178.8, 190.7, 211.5, 232.3, 253.1, 273.1, 286.7, 288.8, 309.6, 330.5, 350.7, 371.6, 392.4, 413.3, 423.1, 428.9, 432.7]

win_size_buffer=[1, 2, 4, 8, 4, 8, 16, 32, 64, 128, 256, 512, 256, 512, 256, 512, 256, 512, 512, 512, 256, 128, 256, 128, 64, 128, 256, 512, 256, 512, 512, 512]
win_size_time_buffer=[0, 0.0, 0.9, 2.2, 4.3, 5.7, 7.8, 11.5, 18.5, 25.3, 46.1, 66.9, 87.8, 102.1, 122.9, 143.4, 164.2, 172.2, 193.0, 213.8, 234.7, 243.1, 245.8, 266.6, 283.6, 295.5, 316.3, 337.1, 357.9, 369.0, 389.8, 410.6]
goodput=[1.0, 0.9900990099009901, 0.9900990099009901, 1.0, 0.9900990099009901, 1.0, 0.9900990099009901, 0.9900990099009901, 1.0, 1.0, 1.0, 0.9900990099009901, 0.9900990099009901, 1.0, 0.9803921568627451, 0.9803921568627451, 1.0, 1.0, 1.0, 0.970873786407767, 0.9512195121951219]
gootput_time=[22.2, 43.7, 64.7, 86.0, 107.0, 127.9, 149.0, 170.5, 191.8, 212.6, 233.4, 254.5, 275.5, 296.8, 318.1, 339.3, 360.2, 381.0, 401.9, 423.9, 432.7]
print(len(win_size_buffer))
print(len(win_size_time_buffer))
#plt.scatter(win_size_time_buffer, win_size_buffer, label= "stars", color= "green", marker= "*", s=30)

plt.figure(figsize=(8,6))
plt.plot(win_size_time_buffer, win_size_buffer)  
# x-axis label
plt.xlabel('time in seconds')
# frequency label
plt.ylabel('window size')
# plot title
plt.title('Window size over time')

plt.figure(figsize=(8,6))
plt.plot(gootput_time, goodput)
plt.xlabel('time in seconds')
plt.ylabel('goodput')
plt.title('goodput over time')

# showing legend
plt.legend()
# function to show the plot
plt.show()




# # x-axis label
# plt.ylim(0,1.2)

# # frequency label

# # showing legend
# plt.legend()
# # function to show the plot
# plt.show()