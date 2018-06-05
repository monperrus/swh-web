import {staticAsset} from 'utils/functions';

function setBrandImage(imgPath) {
  $('.swh-sidebar .brand-image').attr('src', staticAsset(imgPath));
}

$(document).on('collapsed.lte.pushmenu', event => {
  if ($('body').width() > 980) {
    setBrandImage('img/swh-logo-archive-variant.png');
  }
});

$(document).on('shown.lte.pushmenu', event => {
  setBrandImage('img/swh-logo-archive.png');
});

function ensureNoFooterOverflow() {
  $('body').css('padding-bottom', $('footer').outerHeight() + 'px');
}

$(document).ready(() => {
  // restore previous sidebar state (collapsed/expanded)
  let collapseSidebar = false;
  let previousSidebarState = localStorage.getItem('swh-sidebar-collapsed');
  if (previousSidebarState !== undefined) {
    collapseSidebar = JSON.parse(previousSidebarState);
  }
  if (collapseSidebar) {
    // hack to avoid animated transition for collasping sidebar
    // when loading a page
    let sidebarTransition = $('.main-sidebar, .main-sidebar:before').css('transition');
    let sidebarEltsTransition = $('.sidebar .nav-link p, .main-sidebar .brand-text, .sidebar .user-panel .info').css('transition');
    $('.main-sidebar, .main-sidebar:before').css('transition', 'none');
    $('.sidebar .nav-link p, .main-sidebar .brand-text, .sidebar .user-panel .info').css('transition', 'none');
    $('body').addClass('sidebar-collapse');
    setBrandImage('img/swh-logo-archive-variant.png');
    // restore transitions for user navigation
    setTimeout(() => {
      $('.main-sidebar, .main-sidebar:before').css('transition', sidebarTransition);
      $('.sidebar .nav-link p, .main-sidebar .brand-text, .sidebar .user-panel .info').css('transition', sidebarEltsTransition);
    });
  }

  // redirect to last browse page if any when clicking on the 'Browse' entry
  // in the sidebar
  $(`.swh-browse-link`).click(event => {
    let lastBrowsePage = sessionStorage.getItem('last-browse-page');
    if (lastBrowsePage) {
      event.preventDefault();
      window.location = lastBrowsePage;
    }
  });

  // ensure footer do not overflow main content for mobile devices
  // or after resizing the browser window
  ensureNoFooterOverflow();
  $(window).resize(function() {
    ensureNoFooterOverflow();
    if ($('body').hasClass('sidebar-collapse') && $('body').width() > 980) {
      setBrandImage('img/swh-logo-archive-variant.png');
    }
  });

});

export function initPage(page) {

  $(document).ready(() => {
    // set relevant sidebar link to page active
    $(`.swh-${page}-item`).addClass('active');
    $(`.swh-${page}-link`).addClass('active');

    // triggered when unloading the current page
    window.onunload = () => {
      // backup sidebar state (collapsed/expanded)
      let sidebarCollapsed = $('body').hasClass('sidebar-collapse');
      localStorage.setItem('swh-sidebar-collapsed', JSON.stringify(sidebarCollapsed));
      // backup current browse page
      if (page === 'browse') {
        sessionStorage.setItem('last-browse-page', window.location);
      }
    };

  });
}