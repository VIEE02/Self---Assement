document.getElementById("evaluationForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    // Lấy dữ liệu từ các trường nhập vào
    var memberName = document.getElementById("memberName").value;
    var performance = parseInt(document.getElementById("performance").value);
    var interaction = parseInt(document.getElementById("interaction").value);
    var commitment = parseInt(document.getElementById("commitment").value);
    var professionalism = parseInt(document.getElementById("professionalism").value);
    var development = parseInt(document.getElementById("development").value);
    var diversity = parseInt(document.getElementById("diversity").value);
    
    // Tính điểm trung bình
    var averageRating = (performance + interaction + commitment + professionalism + development + diversity) / 6;
    
    // Hiển thị kết quả
    alert("Đánh giá cho thành viên " + memberName + ":\n" + "Điểm trung bình: " + averageRating.toFixed(2));
    
    // Đặt lại form
    document.getElementById("evaluationForm").reset();
});
