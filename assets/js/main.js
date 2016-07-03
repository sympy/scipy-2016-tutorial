function display_next_event(el) {
    // Display the next event available on meetup.com in the given html element.
    //
    // Usages:
    // Add the following html markup in you page where you want the event to show
    // <div class="section--next_event" data-meetup-url="<name-of-meetup-group-here>"></div>
    //
    // Call this function after the page has loaded.
    // <script> display_next_event('.section--next_event')</script>
    var captions = ["Let's meetup at: ", "Next event:", "Upcoming:", "Next up: "]
    var caption = captions[Math.floor(Math.random()*captions.length)],
        meetup_group = $(el).attr('data-meetup-group');
    $.ajax({
      url: 'https://api.meetup.com/'+meetup_group+'?photo-host=public&sig_id=44948372&only=next_event&sig=03b1cf02afd70a3ae78cc9c8cc83d514d6f37ecf',
      jsonp: 'callback',
      dataType: 'jsonp',
      success: function( response ) {
          var next_event = response.data.next_event
          // display only when there is an event.
          if (next_event){
            var html = '<span class=caption>'+ caption +'</span><a target="_blank" href=http://www.meetup.com/'+meetup_group+'/events/' + next_event.id + ' >' + next_event.name + '</a>';
            $(el).html(html).css({'opacity': 1});
          };
      }
    });
}
