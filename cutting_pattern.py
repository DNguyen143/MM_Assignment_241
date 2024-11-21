def find_vectors_recursive_limited(array, n, current_vector, current_sum, index, results, max_results):
    """
    Đệ quy để tìm các vector sao cho tổng (dòng tích) của chúng gần với n nhất và tối đa max_results kết quả.
    """
    # Nếu đã duyệt hết mảng
    if index == len(array):
        if current_sum <= n:
            results.append((current_vector[:], current_sum))
        return

    # Thử tất cả giá trị có thể cho phần tử hiện tại
    for value in range((n - current_sum) // array[index] + 1):
        current_vector.append(value)
        find_vectors_recursive_limited(array, n, current_vector, current_sum + value * array[index], index + 1, results, max_results)
        current_vector.pop()  # Backtrack

def find_top_k_vectors(array, n, max_results=1000):
    """
    Tìm tối đa max_results vector (hệ số) sao cho tổng của chúng bé hơn hoặc bằng n và gần n nhất.
    """
    results = []
    find_vectors_recursive_limited(array, n, [], 0, 0, results, max_results)

    # Sắp xếp các kết quả theo khoảng cách từ tổng tích đến n
    results.sort(key=lambda x: abs(n - x[1]), reverse=False)
    
    # Chỉ lấy tối đa max_results vector
    top_results = [vec for vec, _ in results[:max_results]]
    return top_results


def can_fit_all(h, w, rectangles):
    """
    Kiểm tra xem hình chữ nhật kích thước h x w có chứa được danh sách các hình chữ nhật con mà không chồng lấn.

    :param h: Chiều cao của hình chữ nhật lớn.
    :param w: Chiều rộng của hình chữ nhật lớn.
    :param rectangles: Danh sách các hình chữ nhật con (dạng [(m1, n1), (m2, n2), ...]).
    :return: True nếu có thể chứa được tất cả mà không chồng lấn, ngược lại False.
    """
    # Bước 1: Kiểm tra tổng diện tích
    total_area = sum(m * n for m, n in rectangles)
    if total_area > h * w:
        return False  # Nếu tổng diện tích lớn hơn diện tích hình chữ nhật lớn, không thể chứa

    # Bước 2: Thử xếp các hình chữ nhật vào hình lớn
    # Sắp xếp các hình chữ nhật con theo diện tích giảm dần (để tối ưu việc sắp xếp)
    rectangles = sorted(rectangles, key=lambda x: max(x), reverse=True)

    # Bàn cờ kích thước h x w để kiểm tra
    grid = [[False] * w for _ in range(h)]

    def place_rectangle(m, n):
        """
        Thử đặt một hình chữ nhật kích thước m x n vào hình chữ nhật lớn.
        :return: True nếu đặt được, ngược lại False.
        """
        for i in range(h - m + 1):  # Duyệt qua từng vị trí có thể đặt theo chiều cao
            for j in range(w - n + 1):  # Duyệt qua từng vị trí có thể đặt theo chiều rộng
                # Kiểm tra ô trống
                if all(
                    not grid[i + x][j + y]
                    for x in range(m)
                    for y in range(n)
                ):
                    # Đánh dấu đã sử dụng các ô
                    for x in range(m):
                        for y in range(n):
                            grid[i + x][j + y] = True
                    return True
        return False

    for m, n in rectangles:
        # Thử đặt hình chữ nhật (m, n) hoặc xoay (n, m)
        if not (place_rectangle(m, n) or place_rectangle(n, m)):
            return False  # Nếu không đặt được, trả về False

    return True  # Nếu đặt được tất cả, trả về True
def find_cutting_pattern(rectangles, vectors, h, w): 
    temp = []
    result = []
    for vector in vectors:
        for i in range(0, len(vector)):
            for j in range(0, vector[i]):
                temp.append(rectangles[i])
        if can_fit_all(h,w, temp):
            #print(vector)
            result.append(vector)
            #print("fit")
        #print(temp)
        temp = []
    #print(result)
    return result


# Ví dụ sử dụng
h = 24
w = 14
rectangles = [(2, 1), (4, 2), (5, 3), (7,4), (8,5)]  # Danh sách các hình chữ nhật con
array = [2, 8, 15, 28, 40]
n = 100

vectors = find_top_k_vectors(array, n, max_results=10000000)
print(find_cutting_pattern(rectangles, vectors, h, w))
#temp = []
#v = [8, 10, 2, 3, 2]
#for i in range(5):
#    for j in range(v[i]):
#        temp.append(rectangles[i])
#print()
#print(can_fit_all(h, w, temp))
