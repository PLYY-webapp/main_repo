// 플리 카드
function fetchPlyy(api_route) {
    const sessionId = document.getElementById('session-data').getAttribute('data-session-id');
    fetch(api_route)
    .then(response => response.json())
    .then(data => {
        data.forEach((plyy, index) => {
            let dateTagId = 'dateTag' + index;
            let plyyTagId = 'plyyTag' + index;
            const plyyCard = document.createElement('li');
            plyyCard.innerHTML = 
                `<a href="/plyy/${plyy.id}">` +
                    '<div class="plyy-card__top">' +
                        `<img src="/static/cardimage/${plyy.img}" alt="" class="plyy-card__top__img">` +
                        `<div id="${dateTagId}" class="badge green"></div>` + 
                        '<div class="plyy-card__top__tag-list">' +
                            `<div class="badge tag"># ${plyy.genre}</div>` +
                            `<div id="${plyyTagId}" class="badge tag"></div>` +
                        '</div>' +
                        `<button class="btn-plike--${plyy.pliked ? 'fill' : 'unfill'}" id="like-${plyy.id}" aria-label="플레이리스트 좋아요 즐겨찾기"></button>` +
                    '</div>' +
                    '<div class="plyy-card__bottom">' +
                        '<div>' +
                            `<div class="plyy-card__bottom__title fs16"><span class="hide">${plyy.title}</span>${plyy.title}</div>` +
                            '<div class="align both">' +
                                `<div class="plyy-card__bottom--cname fs12"><span class="hide">${plyy.curator}</span>${plyy.curator}</div>` +
                                `<div class="plyy-card__bottom--count fs12"><span class="hide">${plyy.tracks}곡 | ${plyy_time(plyy.times)}</span>${plyy.tracks}곡 | ${plyy_time(plyy.times)}</div>` +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</a>';
            mainList.appendChild(plyyCard);

            // NEW | UPDATE 태그
            let dateTag = document.getElementById(dateTagId);
            isDate = isTag(plyy.generate, plyy.update);
            if (isDate) {
                dateTag.innerHTML = '<span class="hide">' + isDate + '</span>' + isDate;
            } else {
                dateTag.style.visibility = "hidden";
            };
            
            // 플리태그 2개까지
            let plyy_tag = document.getElementById(plyyTagId);
            if (plyy.tag) {
                plyy_tag.textContent = '#' + plyy.tag;
            } else {
                plyy_tag.style.visibility = "hidden";
            };

            // 플레이리스트 좋아요 버튼 클릭 이벤트 처리
            const likeButton = document.getElementById(`like-${plyy.id}`);
            likeButton.addEventListener('click', function(event) {
                event.preventDefault();
                const pid = plyy.id;
                if (sessionId) {
                    PlaylistToggleLike(sessionId, pid);
                } else {
                    alert('로그인이 필요합니다.');
                }
            });
        });
    })
    .catch(error => console.error('데이터를 처리하는 과정에서 오류가 발생하였습니다.', error));
};
