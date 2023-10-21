document.getElementById('studentForm').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent form submission

  // Get form values
  var name = document.getElementById('name').value;
  var mis = document.getElementById('mis').value;
  var attendance = document.getElementById('attendance').value;
  var academics = document.getElementById('academics').value;
  var extra = document.getElementById('extra').value;

  // Create CSV content
  var csvContent = "data:text/csv;charset=utf-8,"
    + "Name,MIS,Attendance (%),CGPA,Extra Curricular\n"
    + name + "," + mis + "," + attendance + "," + academics + "," + extra;

  // Create a temporary link element to download the CSV file
  var link = document.createElement('a');
  link.href = encodeURI(csvContent);
  link.target = '_blank';
  link.download = 'student_info.csv';
  document.body.appendChild(link);

  // Simulate a click on the link to trigger the download
  link.click();

  // Clean up
  document.body.removeChild(link);
});

