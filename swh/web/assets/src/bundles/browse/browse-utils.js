/**
 * Copyright (C) 2018  The Software Heritage developers
 * See the AUTHORS file at the top-level directory of this distribution
 * License: GNU Affero General Public License version 3, or any later version
 * See top-level LICENSE file for more information
 */

$(document).ready(() => {

  $('.dropdown-submenu a.dropdown-item').on('click', e => {
    $(e.target).next('div').toggle();
    if ($(e.target).next('div').css('display') !== 'none') {
      $(e.target).focus();
    } else {
      $(e.target).blur();
    }
    e.stopPropagation();
    e.preventDefault();
  });

  $('.swh-metadata-toggler').popover({
    boundary: 'viewport',
    container: 'body',
    html: true,
    template: `<div class="popover" role="tooltip">
                   <div class="arrow"></div>
                   <h3 class="popover-header"></h3>
                   <div class="popover-body swh-metadata"></div>
                 </div>`,
    content: function() {
      var content = $(this).attr('data-popover-content');
      return $(content).children('.popover-body').html();
    },
    title: function() {
      var title = $(this).attr('data-popover-content');
      return $(title).children('.popover-heading').html();
    },
    offset: '50vh'
  });

  $('.swh-vault-menu a.dropdown-item').on('click', e => {
    $('.swh-metadata-toggler').popover('hide');
  });

  $('.swh-metadata-toggler').on('show.bs.popover', () => {
    $('.swh-vault-menu .dropdown-menu').hide();
  });

  $('.swh-actions-dropdown').on('hide.bs.dropdown', () => {
    $('.swh-vault-menu .dropdown-menu').hide();
    $('.swh-metadata-toggler').popover('hide');
  });

  $('body').on('click', e => {
    if ($(e.target).parents('.swh-metadata').length) {
      e.stopPropagation();
    }
  });

});