# -*- coding: utf-8 -*-
"""
Nội dung Học liệu số (HLS) — Học phần EC1103 "Kỹ năng giao tiếp và soạn thảo văn bản".
Phần phân công của GV Đỗ Thùy Hương: Chương 4 + Bài thực hành 2 & 3.

Mỗi "deck" gồm:
  title        : tên hiển thị trên trang bìa (dòng phụ đề)
  objectives   : 4 mục tiêu (slide MỤC TIÊU)
  contents     : tối đa 5 mục lớn (slide NỘI DUNG)
  sections     : các slide nội dung thân bài; mỗi mục có points[≤4], sidebar[4], narration
  case         : tình huống thực tiễn (desc + 3 câu hỏi)
  discussion   : câu hỏi thảo luận
  exercise     : bài tập vận dụng (noidung/yeucau/huongdan/thoigian)
  summary      : tổng kết (points[4] + sidebar[4])
  narr_*       : lời thuyết minh cho các slide khung
Nội dung bám Nghị định 30/2020/NĐ-CP về công tác văn thư và thực tiễn VB thương mại.
"""

COURSE = "KỸ NĂNG GIAO TIẾP VÀ SOẠN THẢO VĂN BẢN"

# =====================================================================
# CHƯƠNG 4: SOẠN THẢO VÀ TRÌNH BÀY VĂN BẢN
# =====================================================================
CHUONG4 = {
    "key": "Chuong4",
    "title": "CHƯƠNG 4: SOẠN THẢO VÀ TRÌNH BÀY VĂN BẢN",
    "objectives": [
        "Hiểu được khái niệm, vai trò và cách phân loại văn bản",
        "Phân tích yêu cầu nội dung và 9 thành phần thể thức theo Nghị định 30/2020/NĐ-CP",
        "Vận dụng soạn thảo các văn bản hành chính và thương mại thông dụng",
        "Giải quyết tình huống soạn thảo trong môi trường công sở – kinh doanh",
    ],
    "contents": [
        "Khái niệm và phân loại văn bản",
        "Các yêu cầu về nội dung và thể thức văn bản",
        "Soạn thảo văn bản hành chính thông dụng",
        "Soạn thảo văn bản thương mại",
    ],
    "narr_title": (
        "Xin chào các anh chị học viên. Chào mừng các anh chị đến với Chương 4 của học phần "
        "Kỹ năng giao tiếp và soạn thảo văn bản, với chủ đề Soạn thảo và trình bày văn bản. "
        "Đây là chương đặt nền tảng cho toàn bộ kỹ năng soạn thảo mà chúng ta sẽ thực hành ở các bài tiếp theo."
    ),
    "narr_objectives": (
        "Sau khi học xong chương này, các anh chị sẽ hiểu được văn bản là gì và được phân loại ra sao; "
        "phân tích được yêu cầu về nội dung cùng chín thành phần thể thức bắt buộc theo Nghị định 30 năm 2020; "
        "vận dụng để soạn các văn bản hành chính và thương mại thông dụng; và xử lý được những tình huống "
        "soạn thảo thường gặp nơi công sở và doanh nghiệp."
    ),
    "narr_contents": (
        "Chương 4 gồm bốn nội dung chính. Thứ nhất, khái niệm và phân loại văn bản. Thứ hai, các yêu cầu "
        "về nội dung và thể thức. Thứ ba, soạn thảo văn bản hành chính thông dụng. Và thứ tư, soạn thảo "
        "văn bản thương mại. Chúng ta sẽ đi lần lượt từng phần."
    ),
    "sections": [
        {
            "title": "4.1. KHÁI NIỆM VÀ PHÂN LOẠI VĂN BẢN",
            "points": [
                "Văn bản: phương tiện ghi và truyền đạt thông tin bằng ngôn ngữ hoặc ký hiệu nhất định",
                "Vai trò: công cụ quản lý, giao dịch và lưu trữ thông tin chính thức của tổ chức",
                "Phân loại theo NĐ 30/2020: văn bản hành chính và văn bản chuyên ngành",
                "Nhóm thông dụng: Quyết định, Công văn, Tờ trình, Biên bản, Báo cáo, Thông báo…",
            ],
            "sidebar": ["Khái niệm", "Vai trò", "Phân loại", "Ví dụ"],
            "narration": (
                "Trước hết, văn bản là phương tiện ghi lại và truyền đạt thông tin bằng ngôn ngữ hoặc ký hiệu "
                "nhất định. Trong tổ chức, văn bản giữ ba vai trò quan trọng: là công cụ quản lý điều hành, là "
                "phương tiện giao dịch, và là cơ sở để lưu trữ thông tin chính thức có giá trị pháp lý. "
                "Theo Nghị định 30 năm 2020, văn bản được chia thành hai nhóm lớn: văn bản hành chính và văn bản "
                "chuyên ngành. Trong phạm vi học phần, chúng ta tập trung vào nhóm văn bản hành chính thông dụng "
                "như Quyết định, Công văn, Tờ trình, Biên bản, Báo cáo và Thông báo. Việc nhận diện đúng loại văn "
                "bản sẽ giúp chúng ta chọn đúng bố cục và văn phong khi soạn thảo."
            ),
        },
        {
            "title": "4.2. YÊU CẦU VỀ NỘI DUNG VÀ THỂ THỨC",
            "points": [
                "Nội dung: đúng thẩm quyền, đúng pháp luật, rõ ràng, súc tích, đủ ý",
                "9 thành phần thể thức bắt buộc theo Nghị định 30/2020/NĐ-CP",
                "Kỹ thuật trình bày: khổ A4, phông Times New Roman cỡ 13–14, canh lề chuẩn",
                "Nguyên tắc: thống nhất, chính xác, trang trọng và lịch sự",
            ],
            "sidebar": ["Nội dung", "Thể thức", "Kỹ thuật", "Lưu ý"],
            "narration": (
                "Một văn bản đạt yêu cầu phải đảm bảo cả về nội dung lẫn thể thức. Về nội dung, văn bản phải đúng "
                "thẩm quyền ban hành, phù hợp pháp luật, trình bày rõ ràng, súc tích và đủ ý. Về thể thức, Nghị định "
                "30 năm 2020 quy định chín thành phần bắt buộc, gồm: quốc hiệu và tiêu ngữ; tên cơ quan ban hành; "
                "số và ký hiệu văn bản; địa danh và thời gian ban hành; tên loại và trích yếu nội dung; nội dung văn "
                "bản; chức vụ, chữ ký và họ tên người ký; dấu hoặc chữ ký số; và nơi nhận. Về kỹ thuật trình bày, văn "
                "bản dùng khổ giấy A4, phông chữ Times New Roman cỡ 13 đến 14, canh lề theo chuẩn: trên và dưới khoảng "
                "20 đến 25 milimet, lề trái 30 đến 35, lề phải 15 đến 20 milimet. Nguyên tắc xuyên suốt là thống nhất, "
                "chính xác, trang trọng và lịch sự."
            ),
        },
        {
            "title": "4.3. SOẠN THẢO VĂN BẢN HÀNH CHÍNH THÔNG DỤNG",
            "points": [
                "Quyết định: văn bản cá biệt, bố cục Căn cứ – Quyết định – Điều khoản thi hành",
                "Công văn: trao đổi, đề nghị, trả lời công việc; có trích yếu nội dung",
                "Tờ trình: đề xuất cấp trên xem xét, phê duyệt một nội dung cụ thể",
                "Biên bản và Báo cáo: ghi nhận sự việc / tổng hợp, đánh giá tình hình",
            ],
            "sidebar": ["Quyết định", "Công văn", "Tờ trình", "Biên bản"],
            "narration": (
                "Trong nhóm văn bản hành chính, chúng ta cần thành thạo một số loại thông dụng. Quyết định là văn "
                "bản cá biệt dùng để áp dụng pháp luật, có bố cục ba phần: phần căn cứ, phần quyết định và phần điều "
                "khoản thi hành. Công văn dùng để trao đổi, đề nghị hoặc trả lời công việc giữa các cơ quan, luôn có "
                "phần trích yếu nội dung. Tờ trình dùng để đề xuất cấp trên xem xét, phê duyệt một vấn đề cụ thể. "
                "Biên bản dùng để ghi nhận trung thực một sự việc đang hoặc vừa diễn ra, còn Báo cáo dùng để tổng hợp, "
                "đánh giá tình hình thực hiện công việc. Mỗi loại sẽ được hướng dẫn chi tiết kèm mẫu trong bài thực hành."
            ),
        },
        {
            "title": "4.4. SOẠN THẢO VĂN BẢN THƯƠNG MẠI",
            "points": [
                "Khái niệm: văn bản phục vụ giao dịch kinh doanh giữa các chủ thể",
                "Thư tín thương mại: chào hàng, hỏi hàng, đặt hàng, khiếu nại, phúc đáp…",
                "Báo giá: cung cấp thông tin giá và điều kiện mua bán",
                "Hợp đồng, biên bản nghiệm thu và thanh lý hợp đồng",
            ],
            "sidebar": ["Khái niệm", "Thư tín", "Báo giá", "Hợp đồng"],
            "narration": (
                "Bên cạnh văn bản hành chính, trong môi trường kinh doanh chúng ta thường xuyên sử dụng văn bản "
                "thương mại. Đây là loại văn bản phục vụ trực tiếp cho hoạt động giao dịch giữa các chủ thể kinh doanh. "
                "Thư tín thương mại bao gồm nhiều dạng như thư chào hàng, hỏi hàng, đặt hàng, khiếu nại và phúc đáp. "
                "Báo giá là văn bản cung cấp thông tin về giá cả và điều kiện mua bán cho khách hàng. Hợp đồng là sự "
                "thỏa thuận ràng buộc quyền và nghĩa vụ giữa các bên, thường đi kèm biên bản nghiệm thu và biên bản "
                "thanh lý khi kết thúc. Các loại văn bản này sẽ được thực hành kỹ trong Bài 3."
            ),
        },
    ],
    "case": {
        "desc": ("Công ty TNHH An Phát cần bổ nhiệm một trưởng phòng kinh doanh mới và thông báo "
                 "việc thay đổi đầu mối liên hệ đến các đối tác."),
        "questions": [
            "Cần soạn thảo những loại văn bản nào cho tình huống trên?",
            "Mỗi văn bản phải bảo đảm những thành phần thể thức bắt buộc nào?",
            "Những lỗi trình bày nào thường khiến văn bản bị trả lại?",
        ],
        "narration": (
            "Hãy cùng phân tích một tình huống thực tế. Công ty An Phát cần bổ nhiệm một trưởng phòng kinh doanh "
            "mới, đồng thời thông báo việc thay đổi đầu mối liên hệ tới các đối tác. Các anh chị hãy suy nghĩ: tình "
            "huống này cần những loại văn bản nào; mỗi văn bản phải có đủ thành phần thể thức gì; và những lỗi trình "
            "bày nào thường khiến văn bản bị trả lại để chỉnh sửa. Chúng ta sẽ cùng trao đổi ở phần thảo luận."
        ),
    },
    "discussion": {
        "q": "Theo anh/chị, lỗi thể thức nào khiến một văn bản hành chính bị xem là không hợp lệ? Cho ví dụ minh họa.",
        "narration": (
            "Câu hỏi thảo luận của chúng ta: theo anh chị, lỗi thể thức nào khiến một văn bản hành chính bị xem là "
            "không hợp lệ? Hãy nêu một ví dụ cụ thể mà anh chị từng gặp và đề xuất cách khắc phục. Mời các anh chị "
            "ghi câu trả lời vào diễn đàn của lớp trên hệ thống E-learning."
        ),
    },
    "exercise": {
        "noidung": "Soạn thảo 01 Công văn mời họp của Khoa Kinh tế – Luật gửi đến các bộ môn trực thuộc.",
        "yeucau": "Đúng và đủ 9 thành phần thể thức; văn phong hành chính chuẩn mực, súc tích.",
        "huongdan": "Trình bày theo mẫu Nghị định 30/2020; nộp file Word (.docx) trên E-learning.",
        "thoigian": "Hoàn thành và nộp trong vòng 01 tuần.",
        "narration": (
            "Để vận dụng kiến thức của chương, các anh chị hãy soạn một Công văn mời họp của Khoa Kinh tế – Luật gửi "
            "tới các bộ môn. Yêu cầu là trình bày đúng và đủ chín thành phần thể thức, văn phong hành chính chuẩn mực. "
            "Các anh chị làm theo mẫu của Nghị định 30, nộp file Word trên E-learning trong vòng một tuần."
        ),
    },
    "summary": {
        "points": [
            "Văn bản: khái niệm, vai trò và cách phân loại",
            "Chín thành phần thể thức bắt buộc theo NĐ 30/2020",
            "Các văn bản hành chính thông dụng và bố cục",
            "Các văn bản thương mại cơ bản trong kinh doanh",
        ],
        "sidebar": ["Khái niệm", "Phân loại", "Thể thức", "Soạn thảo"],
        "narration": (
            "Tóm lại, Chương 4 đã giúp chúng ta nắm được khái niệm, vai trò và cách phân loại văn bản; chín thành phần "
            "thể thức bắt buộc theo Nghị định 30; bố cục của các văn bản hành chính thông dụng; và các văn bản thương "
            "mại cơ bản. Đây là nền tảng để chúng ta bước vào phần thực hành soạn thảo ở Bài 2 và Bài 3. Cảm ơn các anh chị."
        ),
    },
}

# =====================================================================
# BÀI 2 (THỰC HÀNH): SOẠN THẢO VĂN BẢN HÀNH CHÍNH
# =====================================================================
BAI2 = {
    "key": "Bai2",
    "title": "BÀI 2 (THỰC HÀNH): SOẠN THẢO VĂN BẢN HÀNH CHÍNH",
    "objectives": [
        "Nắm bố cục và thể thức chuẩn của từng loại văn bản hành chính",
        "Phân biệt được mục đích sử dụng của Quyết định, Tờ trình, Công văn, Biên bản, Báo cáo",
        "Soạn thảo thành thạo theo mẫu chuẩn của Nghị định 30/2020/NĐ-CP",
        "Tự kiểm tra, chỉnh sửa văn bản theo phản hồi của giảng viên",
    ],
    "contents": [
        "Soạn thảo Quyết định",
        "Soạn thảo Tờ trình",
        "Soạn thảo các loại Công văn",
        "Soạn thảo Biên bản",
        "Soạn thảo Báo cáo",
    ],
    "narr_title": (
        "Xin chào các anh chị. Đây là Bài thực hành số 2 của học phần: Soạn thảo văn bản hành chính. Ở bài này, "
        "với mỗi loại văn bản, chúng ta sẽ ôn nhanh lý thuyết, xem một mẫu cụ thể, rồi thực hành ngay."
    ),
    "narr_objectives": (
        "Mục tiêu của bài thực hành là giúp các anh chị nắm vững bố cục và thể thức của từng loại văn bản hành chính, "
        "phân biệt được khi nào dùng loại nào, soạn thảo thành thạo theo mẫu chuẩn, và biết tự rà soát, chỉnh sửa "
        "văn bản theo góp ý."
    ),
    "narr_contents": (
        "Bài 2 hướng dẫn soạn năm loại văn bản hành chính thông dụng: Quyết định, Tờ trình, các loại Công văn, "
        "Biên bản và Báo cáo. Với mỗi loại, tôi sẽ giới thiệu qua một mẫu và giao một bài tập nhỏ."
    ),
    "sections": [
        {
            "title": "2.1. SOẠN THẢO QUYẾT ĐỊNH",
            "points": [
                "Dùng để ban hành, bổ nhiệm, khen thưởng, xử lý… (văn bản cá biệt)",
                "Bố cục: phần Căn cứ – phần Quyết định – phần Điều khoản thi hành",
                "Các điều được đánh số: Điều 1, Điều 2, … rõ ràng, ngắn gọn",
                "Mẫu: Quyết định bổ nhiệm / khen thưởng theo NĐ 30/2020",
            ],
            "sidebar": ["Mục đích", "Bố cục", "Trình bày", "Mẫu"],
            "narration": (
                "Loại đầu tiên là Quyết định. Quyết định là văn bản cá biệt, dùng để ban hành, bổ nhiệm, khen thưởng "
                "hoặc xử lý một việc cụ thể. Bố cục gồm ba phần: phần căn cứ mở đầu bằng các cụm Căn cứ…; phần quyết "
                "định trình bày thành các điều được đánh số Điều 1, Điều 2; và phần điều khoản thi hành nêu rõ ai chịu "
                "trách nhiệm thi hành và hiệu lực. Các anh chị xem mẫu Quyết định bổ nhiệm trên màn hình, chú ý cách "
                "viết phần căn cứ và cách đánh số các điều."
            ),
        },
        {
            "title": "2.2. SOẠN THẢO TỜ TRÌNH",
            "points": [
                "Dùng để đề xuất cấp trên xem xét, phê duyệt một nội dung",
                "Bố cục: lý do/sự cần thiết – nội dung đề xuất – kiến nghị",
                "Lập luận chặt chẽ, có số liệu, nêu rõ phương án",
                "Mẫu: Tờ trình xin kinh phí / phê duyệt kế hoạch",
            ],
            "sidebar": ["Mục đích", "Bố cục", "Lập luận", "Mẫu"],
            "narration": (
                "Loại thứ hai là Tờ trình, dùng để đề xuất cấp trên xem xét và phê duyệt một nội dung. Một tờ trình "
                "thuyết phục cần ba phần: nêu lý do và sự cần thiết, trình bày nội dung đề xuất, và đưa ra kiến nghị "
                "cụ thể. Điểm mấu chốt là lập luận chặt chẽ, có số liệu minh chứng và nêu rõ phương án. Mời các anh "
                "chị tham khảo mẫu Tờ trình xin kinh phí."
            ),
        },
        {
            "title": "2.3. SOẠN THẢO CÁC LOẠI CÔNG VĂN",
            "points": [
                "Công văn đề nghị, trả lời, đôn đốc, mời họp, hướng dẫn…",
                "Đặc trưng: không có tên loại, dùng số/ký hiệu và trích yếu",
                "Văn phong lịch sự, mỗi công văn một chủ đề",
                "Mẫu: Công văn mời họp / đề nghị phối hợp",
            ],
            "sidebar": ["Phân loại", "Đặc trưng", "Văn phong", "Mẫu"],
            "narration": (
                "Loại thứ ba là Công văn. Công văn rất đa dạng: công văn đề nghị, trả lời, đôn đốc, mời họp hay hướng "
                "dẫn. Đặc trưng của công văn là không ghi tên loại văn bản, mà dùng số, ký hiệu kèm phần trích yếu nội "
                "dung. Mỗi công văn chỉ nên giải quyết một chủ đề, với văn phong lịch sự, rõ ràng. Các anh chị xem mẫu "
                "Công văn mời họp và để ý phần trích yếu."
            ),
        },
        {
            "title": "2.4. SOẠN THẢO BIÊN BẢN",
            "points": [
                "Ghi nhận trung thực, khách quan một sự việc đang/đã diễn ra",
                "Thành phần: thời gian, địa điểm, thành phần tham dự, diễn biến, kết luận",
                "Có chữ ký của các bên liên quan để xác nhận",
                "Mẫu: Biên bản cuộc họp / bàn giao",
            ],
            "sidebar": ["Mục đích", "Thành phần", "Xác nhận", "Mẫu"],
            "narration": (
                "Loại thứ tư là Biên bản, dùng để ghi nhận trung thực và khách quan một sự việc. Một biên bản đầy đủ "
                "cần có: thời gian, địa điểm, thành phần tham dự, diễn biến nội dung và phần kết luận. Cuối biên bản "
                "phải có chữ ký xác nhận của các bên liên quan để bảo đảm giá trị. Mời các anh chị xem mẫu Biên bản "
                "cuộc họp."
            ),
        },
        {
            "title": "2.5. SOẠN THẢO BÁO CÁO",
            "points": [
                "Tổng hợp, đánh giá tình hình, kết quả thực hiện công việc",
                "Bố cục: đặt vấn đề – kết quả/nội dung – đánh giá, kiến nghị",
                "Số liệu trung thực, có so sánh, bám mục tiêu",
                "Mẫu: Báo cáo tổng kết / báo cáo định kỳ",
            ],
            "sidebar": ["Mục đích", "Bố cục", "Số liệu", "Mẫu"],
            "narration": (
                "Loại cuối cùng của bài là Báo cáo, dùng để tổng hợp và đánh giá tình hình hoặc kết quả công việc. "
                "Bố cục gồm: đặt vấn đề, trình bày kết quả hoặc nội dung chính, và phần đánh giá kèm kiến nghị. Báo "
                "cáo cần số liệu trung thực, có so sánh và bám sát mục tiêu đề ra. Các anh chị tham khảo mẫu Báo cáo "
                "tổng kết để thực hành."
            ),
        },
    ],
    "case": {
        "desc": ("Phòng Đào tạo cần tổ chức một cuộc họp triển khai kế hoạch học kỳ và lập biên bản, "
                 "sau đó báo cáo kết quả lên Ban Giám hiệu."),
        "questions": [
            "Chuỗi văn bản nào cần được soạn theo đúng trình tự?",
            "Công văn mời họp và Biên bản khác nhau ở thể thức nào?",
            "Báo cáo cần những số liệu gì để thuyết phục?",
        ],
        "narration": (
            "Hãy xét một tình huống xâu chuỗi nhiều loại văn bản. Phòng Đào tạo cần tổ chức họp triển khai kế hoạch "
            "học kỳ, lập biên bản, rồi báo cáo kết quả lên Ban Giám hiệu. Các anh chị thử xác định trình tự văn bản "
            "cần soạn, điểm khác nhau về thể thức giữa công văn mời họp và biên bản, và những số liệu cần có trong báo cáo."
        ),
    },
    "discussion": {
        "q": "Khi nào dùng Công văn, khi nào phải dùng Quyết định? Cho ví dụ trong thực tế công việc của anh/chị.",
        "narration": (
            "Mời các anh chị thảo luận: khi nào nên dùng Công văn và khi nào bắt buộc phải dùng Quyết định? Hãy nêu "
            "ví dụ từ chính công việc của mình và đăng lên diễn đàn lớp."
        ),
    },
    "exercise": {
        "noidung": "BÀI TẬP 2: Soạn 01 Quyết định khen thưởng và 01 Công văn mời họp theo tình huống được giao.",
        "yeucau": "Đúng bố cục từng loại, đủ 9 thành phần thể thức, không sai chính tả – văn phong.",
        "huongdan": "Dựa trên mẫu đã giới thiệu; nộp 02 file Word trên E-learning, đặt tên theo mã số học viên.",
        "thoigian": "Hoàn thành trong 01 tuần, có thể chỉnh sửa 01 lần theo phản hồi.",
        "narration": (
            "Bài tập của Bài 2: các anh chị hãy soạn một Quyết định khen thưởng và một Công văn mời họp theo tình "
            "huống được giao. Yêu cầu đúng bố cục từng loại, đủ chín thành phần thể thức, không sai chính tả và văn "
            "phong. Các anh chị dựa trên mẫu đã giới thiệu, nộp hai file Word trên E-learning trong một tuần."
        ),
    },
    "summary": {
        "points": [
            "Quyết định và Tờ trình: bố cục và mục đích",
            "Các loại Công văn và phần trích yếu đặc trưng",
            "Biên bản: ghi nhận và xác nhận sự việc",
            "Báo cáo: tổng hợp, đánh giá có số liệu",
        ],
        "sidebar": ["Quyết định", "Công văn", "Biên bản", "Báo cáo"],
        "narration": (
            "Tóm lại, Bài 2 đã hướng dẫn các anh chị soạn năm loại văn bản hành chính thông dụng cùng mẫu cụ thể. "
            "Hãy luyện tập đều đặn, vì kỹ năng soạn thảo chỉ vững khi được thực hành nhiều lần. Hẹn gặp lại các anh "
            "chị ở Bài 3 về văn bản thương mại."
        ),
    },
}

# =====================================================================
# BÀI 3 (THỰC HÀNH): SOẠN THẢO VĂN BẢN THƯƠNG MẠI
# =====================================================================
BAI3 = {
    "key": "Bai3",
    "title": "BÀI 3 (THỰC HÀNH): SOẠN THẢO VĂN BẢN THƯƠNG MẠI",
    "objectives": [
        "Nắm cấu trúc và văn phong của các văn bản thương mại thông dụng",
        "Soạn được thư tín thương mại và báo giá chuyên nghiệp",
        "Hiểu các điều khoản cơ bản của hợp đồng và biên bản kèm theo",
        "Vận dụng vào tình huống giao dịch kinh doanh thực tế",
    ],
    "contents": [
        "Soạn thảo thư tín thương mại",
        "Soạn thảo báo giá",
        "Soạn thảo Hợp đồng, biên bản nghiệm thu và thanh lý hợp đồng",
    ],
    "narr_title": (
        "Xin chào các anh chị. Đây là Bài thực hành số 3: Soạn thảo văn bản thương mại. Khác với văn bản hành chính, "
        "văn bản thương mại hướng tới hiệu quả giao dịch và xây dựng quan hệ với khách hàng, đối tác."
    ),
    "narr_objectives": (
        "Mục tiêu của bài là giúp các anh chị nắm cấu trúc và văn phong của các văn bản thương mại; soạn được thư tín "
        "thương mại và báo giá chuyên nghiệp; hiểu các điều khoản cơ bản của hợp đồng cùng biên bản nghiệm thu, thanh "
        "lý; và vận dụng vào tình huống giao dịch thực tế."
    ),
    "narr_contents": (
        "Bài 3 gồm ba nội dung: thư tín thương mại, báo giá, và hợp đồng kèm biên bản nghiệm thu, thanh lý. Mỗi nội "
        "dung đều có mẫu minh họa và bài tập đi kèm."
    ),
    "sections": [
        {
            "title": "3.1. SOẠN THẢO THƯ TÍN THƯƠNG MẠI",
            "points": [
                "Các dạng: chào hàng, hỏi hàng, đặt hàng, khiếu nại, phúc đáp",
                "Cấu trúc: mở đầu – nội dung – kết thúc lịch sự, kêu gọi hành động",
                "Văn phong: ngắn gọn, lịch sự, hướng tới lợi ích khách hàng",
                "Mẫu: Thư chào hàng / thư phúc đáp khiếu nại",
            ],
            "sidebar": ["Phân loại", "Cấu trúc", "Văn phong", "Mẫu"],
            "narration": (
                "Nội dung đầu tiên là thư tín thương mại. Thư tín có nhiều dạng: chào hàng, hỏi hàng, đặt hàng, khiếu "
                "nại và phúc đáp. Dù ở dạng nào, một bức thư tốt cũng gồm ba phần: mở đầu tạo thiện cảm, phần nội dung "
                "rõ ràng, và phần kết thúc lịch sự kèm lời kêu gọi hành động. Văn phong cần ngắn gọn, lịch sự và luôn "
                "hướng tới lợi ích của khách hàng. Mời các anh chị xem mẫu thư chào hàng."
            ),
        },
        {
            "title": "3.2. SOẠN THẢO BÁO GIÁ",
            "points": [
                "Cung cấp thông tin giá, quy cách, điều kiện bán hàng",
                "Thành phần: thông tin bên bán/mua, bảng giá, điều kiện thanh toán, hiệu lực",
                "Trình bày bảng rõ ràng, nêu rõ đã/chưa gồm thuế VAT",
                "Mẫu: Bảng báo giá sản phẩm/dịch vụ",
            ],
            "sidebar": ["Mục đích", "Thành phần", "Trình bày", "Mẫu"],
            "narration": (
                "Nội dung thứ hai là báo giá. Báo giá cung cấp cho khách hàng thông tin về giá, quy cách và điều kiện "
                "bán hàng. Một báo giá đầy đủ gồm: thông tin bên bán và bên mua, bảng giá chi tiết, điều kiện thanh "
                "toán và thời hạn hiệu lực của báo giá. Các anh chị nên trình bày bảng giá rõ ràng và nêu rõ giá đã "
                "bao gồm hay chưa bao gồm thuế giá trị gia tăng. Tham khảo mẫu bảng báo giá trên màn hình."
            ),
        },
        {
            "title": "3.3. HỢP ĐỒNG, BIÊN BẢN NGHIỆM THU VÀ THANH LÝ",
            "points": [
                "Hợp đồng: thỏa thuận quyền và nghĩa vụ; các điều khoản cơ bản",
                "Điều khoản: chủ thể, đối tượng, giá, thanh toán, quyền-nghĩa vụ, giải quyết tranh chấp",
                "Biên bản nghiệm thu: xác nhận hoàn thành theo hợp đồng",
                "Biên bản thanh lý: kết thúc, đối chiếu nghĩa vụ giữa các bên",
            ],
            "sidebar": ["Hợp đồng", "Điều khoản", "Nghiệm thu", "Thanh lý"],
            "narration": (
                "Nội dung thứ ba là hợp đồng cùng các biên bản đi kèm. Hợp đồng là sự thỏa thuận làm phát sinh quyền "
                "và nghĩa vụ giữa các bên. Một hợp đồng cơ bản gồm các điều khoản: chủ thể ký kết, đối tượng hợp đồng, "
                "giá và phương thức thanh toán, quyền và nghĩa vụ của các bên, và điều khoản giải quyết tranh chấp. "
                "Khi hoàn thành, các bên lập biên bản nghiệm thu để xác nhận kết quả theo hợp đồng, và cuối cùng là "
                "biên bản thanh lý để kết thúc, đối chiếu nghĩa vụ. Đây là bộ ba văn bản gắn liền với mọi giao dịch kinh doanh."
            ),
        },
    ],
    "case": {
        "desc": ("Công ty của anh/chị nhận được thư hỏi hàng từ một khách hàng mới muốn mua 500 sản phẩm, "
                 "yêu cầu báo giá và dự thảo hợp đồng."),
        "questions": [
            "Cần phản hồi bằng những văn bản nào và theo trình tự ra sao?",
            "Báo giá cần nêu rõ những điều kiện gì để tránh tranh chấp?",
            "Những điều khoản nào không thể thiếu trong hợp đồng mua bán?",
        ],
        "narration": (
            "Hãy xét tình huống giao dịch sau. Công ty của các anh chị nhận thư hỏi hàng từ một khách hàng mới muốn "
            "mua 500 sản phẩm và yêu cầu báo giá kèm dự thảo hợp đồng. Các anh chị thử xác định: cần phản hồi bằng "
            "những văn bản nào theo trình tự ra sao; báo giá cần nêu rõ điều kiện gì để tránh tranh chấp; và những "
            "điều khoản nào không thể thiếu trong hợp đồng mua bán."
        ),
    },
    "discussion": {
        "q": "Điều gì tạo nên một thư chào hàng thuyết phục? Theo anh/chị, yếu tố nào quan trọng nhất và vì sao?",
        "narration": (
            "Mời các anh chị thảo luận: điều gì tạo nên một thư chào hàng thuyết phục? Theo anh chị, yếu tố nào là "
            "quan trọng nhất và vì sao? Hãy chia sẻ quan điểm trên diễn đàn của lớp."
        ),
    },
    "exercise": {
        "noidung": "BÀI TẬP 3: Soạn 01 thư chào hàng, 01 báo giá và phác thảo các điều khoản chính của hợp đồng mua bán.",
        "yeucau": "Văn phong thương mại chuyên nghiệp; báo giá đủ điều kiện; điều khoản hợp đồng rõ ràng.",
        "huongdan": "Dựa trên mẫu đã giới thiệu; nộp bộ hồ sơ (Word/PDF) trên E-learning.",
        "thoigian": "Hoàn thành trong 01 tuần, làm việc cá nhân hoặc theo nhóm 2 người.",
        "narration": (
            "Bài tập của Bài 3: các anh chị hãy soạn một thư chào hàng, một bảng báo giá và phác thảo các điều khoản "
            "chính của một hợp đồng mua bán theo tình huống. Yêu cầu văn phong thương mại chuyên nghiệp, báo giá đầy "
            "đủ điều kiện và điều khoản hợp đồng rõ ràng. Nộp bộ hồ sơ trên E-learning trong một tuần."
        ),
    },
    "summary": {
        "points": [
            "Thư tín thương mại: cấu trúc và văn phong",
            "Báo giá: thành phần và cách trình bày",
            "Hợp đồng: các điều khoản cơ bản",
            "Biên bản nghiệm thu và thanh lý hợp đồng",
        ],
        "sidebar": ["Thư tín", "Báo giá", "Hợp đồng", "Biên bản"],
        "narration": (
            "Tóm lại, Bài 3 đã hướng dẫn các anh chị soạn thư tín thương mại, báo giá và bộ văn bản hợp đồng – nghiệm "
            "thu – thanh lý. Đây là những kỹ năng thiết yếu trong môi trường kinh doanh hiện đại. Chúc các anh chị "
            "thực hành hiệu quả. Xin cảm ơn và hẹn gặp lại."
        ),
    },
}

DECKS = [CHUONG4, BAI2, BAI3]
