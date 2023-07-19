import cv2
import numpy as np


def is_white(pixel, threshold):
    return pixel > threshold


def find_closest_group(mask, start_point, threshold, min_group_size):
    height, width = mask.shape

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height

    def get_neighbors(x, y):
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return [(x + dx, y + dy) for dx, dy in moves if is_valid(x + dx, y + dy)]

    def flood_fill(x, y):
        group = []
        queue = [(x, y)]

        while queue:
            curr_x, curr_y = queue.pop()
            group.append((curr_x, curr_y))

            neighbors = get_neighbors(curr_x, curr_y)
            for nx, ny in neighbors:
                if is_valid(nx, ny) and not visited[ny, nx] and is_white(mask[ny, nx], threshold):
                    queue.append((nx, ny))
                    visited[ny, nx] = True

        return group

    visited = np.zeros((height, width), dtype=bool)

    start_x, start_y = start_point
    if not is_valid(start_x, start_y):
        # If the start point is invalid, return None.
        return None

    # Find the connected white region containing the start point.
    white_group = flood_fill(start_x, start_y)

    # Filter out groups that are smaller than the specified threshold.
    white_groups = [group for group in [white_group]
                    if len(group) >= min_group_size]

    if not white_groups:
        return None

    # Compute the centroid of the white group and find the closest group.
    min_distance = float('inf')
    closest_group = None
    for group in white_groups:
        centroid_x = sum(x for x, _ in group) // len(group)
        centroid_y = sum(y for _, y in group) // len(group)
        distance = (start_x - centroid_x) ** 2 + (start_y - centroid_y) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_group = group

    return closest_group

# Example usage:
# Assuming 'mask' is obtained from your findMoveRange function.
# 'point' is a tuple (x, y) representing the coordinates of the point you want to find the closest group for.
# 'threshold' is the pixel value threshold to consider a pixel as white.
# 'min_group_size' is the minimum size (number of white pixels) for a group to be considered.

# closest_white_group = find_closest_group(mask, point, threshold, min_group_size)
