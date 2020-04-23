# def detect_text_for_rem(stats):
#     remaining_text = copy(stats)
#     for stat in remaining_text[:]:
#         if (
#             (stat[2] <= 6 and stat[3] >= 4 * stat[2]) or
#             (stat[3] <= 6 and stat[2] >= 4 * stat[3]) or
#             stat[4] <= 15
#         ):
#             remaining_text.remove(stat)
#     return remaining_text











# # Dilate (to get dilated lines and large connected components):
#     kernel = np.ones((3, 3), np.uint8)
#     dilation_image = cv2.dilate(thresh, kernel, iterations=2)

# # For lines and tables:
# retval_dil, _, stats_np_dil, _ = cv2.connectedComponentsWithStats(dilation_image, connectivity=8)
# stats_np_lines = stats_np_dil[1:retval_dil]