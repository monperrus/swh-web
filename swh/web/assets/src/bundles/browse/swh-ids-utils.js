/**
 * Copyright (C) 2018  The Software Heritage developers
 * See the AUTHORS file at the top-level directory of this distribution
 * License: GNU Affero General Public License version 3, or any later version
 * See top-level LICENSE file for more information
 */

import ClipboardJS from 'clipboard';

$(document).ready(() => {
  new ClipboardJS('.btn-swh-id-copy', {
    text: trigger => {
      let swhId = $(trigger).closest('.swh-id-ui').find('.swh-id').text();
      return swhId;

    }
  });

  new ClipboardJS('.btn-swh-id-url-copy', {
    text: trigger => {
      let swhId = $(trigger).closest('.swh-id-ui').find('.swh-id').text();
      return window.location.origin + '/' + swhId + '/';
    }
  });
});

export function swhIdObjectTypeToggled(event) {
  event.preventDefault();
  $(event.target).tab('show');
}

export function swhIdOptionOriginToggled(event) {
  event.stopPropagation();
  let swhIdElt = $(event.target).closest('.swh-id-ui').find('.swh-id');
  let originPart = ';origin=' + $(event.target).data('swh-origin');
  let currentSwhId = swhIdElt.text();
  if ($(event.target).prop('checked')) {
    currentSwhId += originPart;
  } else {
    currentSwhId = currentSwhId.replace(originPart, '');
  }
  swhIdElt.text(currentSwhId);
  swhIdElt.attr('href', '/' + currentSwhId + '/');
}

export function swhIdOptionLinesToggled(event) {
  event.stopPropagation();
  if (!window.location.hash) {
    return;
  }
  let swhIdElt = $(event.target).closest('.swh-id-ui').find('.swh-id');
  let currentSwhId = swhIdElt.text();
  let lines = [];
  let linesPart = ';lines=';
  let linesRegexp = new RegExp(/L(\d+)/g);
  let line = linesRegexp.exec(window.location.hash);
  while (line) {
    lines.push(parseInt(line[1]));
    line = linesRegexp.exec(window.location.hash);
  }
  if (lines.length > 0) {
    linesPart += lines[0];
  }
  if (lines.length > 1) {
    linesPart += '-' + lines[1];
  }
  if ($(event.target).prop('checked')) {
    currentSwhId += linesPart;
  } else {
    currentSwhId = currentSwhId.replace(linesPart, '');
  }
  swhIdElt.text(currentSwhId);
  swhIdElt.attr('href', '/' + currentSwhId + '/');
}