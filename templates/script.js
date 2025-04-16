$(document).ready(() => {
  let location = { lat: 51.75, lon: 19.45 }; // Budapest, Hungary
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      location.lat = position.coords.latitude;
      location.lon = position.coords.longitude;
    });
  }
  update(location);
  setInterval(() => update(location), 60000);
});

let mapToRange = (num, in_min, in_max, out_min, out_max) => (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

let update = location => $.get('https://api.openweathermap.org/data/2.5/weather?lat=' + location.lat + '&lon=' + location.lon + '&units=metric&appid=d0696f398e113c09c3ca05ac77058264', result => {
  let night = result.dt < result.sys.sunrise || result.dt > result.sys.sunset;
  $('#mercury').css({ 'height': mapToRange(result.main.temp, -20, 50, 0, 68) + '%' }).attr('title', Math.round(result.main.temp) + '°C');
  $('#location').text(result.name);
  $('body').css('background', night ? '#001f3f' : '#7fdbff');
  loadIcon(result.weather[0].id.toString(), result.weather[0].description, night);
});

let loadIcon = (code, text, night) => {
  let iconContainer = $('#icon-container ul');

  // https://webdesignbestfirm.com/forecastfont.html

  if (code.charAt(0) == '2') {
    // thunderstorm
    iconContainer.html('<li class="icon thundercloud"></li><li class="icon thunder"></li>');
  } else if (code.charAt(0) == '3') {
    // drizzle
    iconContainer.html('<li class="icon basecloud"></li><li class="icon drizzle"></li>');
  } else if (code.charAt(0) == '5') {
    // rain
    iconContainer.html('<li class="icon basecloud"></li><li class="icon rain"></li>');
  } else if (code.charAt(0) == '6') {
    // snow
    iconContainer.html('<li class="icon basecloud"></li><li class="icon snow"></li>');
  } else if (code.charAt(0) == '7') {
    // athmosphere
    iconContainer.html('<li class="icon mist"></li>');
  } else if (code.charAt(0) == '8') {
    // clear or clouds
    if (code == '800') {
      iconContainer.html('<li class="icon ' + (!night ? 'sun' : 'moon') + '"></li>');
    } else {
      iconContainer.html('<li class="icon cloud"></li>');
    }
  } else {
    console.log('Invalid weather status');
  }

  iconContainer.attr('title', text);
};

