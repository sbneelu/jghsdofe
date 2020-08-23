function cancelMove() {
  $('.moveable-btn').removeClass('hidden');
  $('.move').addClass('hidden');
  $('#cancel-move').addClass('hidden');
  $('.move-name').html('');
  $('#mid').html('');
}

function moveable(id) {
  $('.moveable-btn').addClass('hidden');
  $('.move').removeClass('hidden');
  $('#cancel-move').removeClass('hidden');
  var mvbl = $(".moveable-title[data-id='" + id + "'] ");
  $('.move-name').html(mvbl.html());
  $('#mid').html(id);
}

function move(order) {
  var id = $('#mid').html();
  $('#mid').html('');
  var mvbl = $('<li class="moveable" data-id="' + id + '"></li>');
  var html = $(".moveable[data-id='" + id + "']").html();
  mvbl.append(html);
  $(".moveable[data-id='" + id + "']").remove();
  var mv = $(".move[data-order='" + order + "']");
  mvbl.insertAfter(mv);

  $('.move').remove();
  $('.moveable-btn').removeClass('hidden');

  var mvbls = $('.moveable');

  var inpval = '';

  var mv = $('<li class="move hidden" data-order="0"></li>');
  var mvbtn = $('<a href="#" class="btn btn-primary move-btn" data-order="0" onclick="move(0);">Move here</a>');

  mv.append(mvbtn);

  $('.moveable-ul').prepend(mv);

  for (var i = 0; i < mvbls.length; i++) {
    var mvbl = mvbls[i];
    inpval += mvbl.getAttribute('data-id') + ',';

    mvbl = $(mvbl);

    var mv = $('<li class="move hidden" data-order="' + (i + 1).toString() + '"></li>');
    var mvbtn = $('<a href="#" class="btn btn-primary move-btn" data-order="' + (i + 1).toString() + '" onclick="move(' + (i + 1).toString() + ');">Move here</a>');

    mv.append(mvbtn);

    mv.insertAfter(mvbl);


  }

  $('#order').val(inpval);

  cancelMove();
}
