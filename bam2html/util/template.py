import string


TEMPLATE = string.Template('''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bam2HTML Result</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/datatables@1.10.17/media/css/jquery.dataTables.min.css">
  <style>
    main .container {
      margin-top: 50px;
    }
    footer {
      font-style: italic;
    }
    footer a {
      color: darkgrey;
    }
    footer a:hover {
      color: red;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <main>
    <div class="container">
      <table id="result" class="table table-hover table-striped">
      </table>
    </div>
  </main>

  <footer class="footer text-center text-muted">
    <div class="container">
      <a href="mailto:suqingdong@novogene.com">contact: suqingdong@novogene.com</a>
      <br>
      <a target="_blank" href="https://github.com/suqingdong/bam2html">source: https://github.com/suqingdong/bam2html</a>
    </div>
  </footer>
</body>
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/datatables@1.10.17/media/js/jquery.dataTables.min.js"></script>
<script>
  var data = ${DATA};
  var columns = [
    {data: 'sample', title: 'SAMPLE'},
    {data: 'site', title: 'SITE'},
    {data: 'html', title: 'HTML'},
  ];

  function init_datatable() {
    $('#result').DataTable({
      data: data,
      columns: columns
    });
  };

  $(document).ready(function() {
    console.log('start ...');
    init_datatable();
  });
</script>
</html>
''')