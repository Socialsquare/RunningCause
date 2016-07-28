$(function() {
  var Spectra = {
    init: function () {
      $.fn.spectragram.accessData = {
        accessToken: '1518270663.8a6c0ce.c414c0ef46d944418816a107b81599b5',
        clientID: '8a6c0ce7701843f7b9e2f939264af531'
      };

      $('#instafeed').spectragram('getUserFeed',{
        max: 8,
        query: 'masangarunners',
        wrapEachWith: '<div class="col-md-3 col-xs-6"></div>'
      });
    }
  }

  Spectra.init();
});
