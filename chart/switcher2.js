var switcher_css = `<style id="switcher-css">
.switcher {
	display: flex;
	align-items: center;
	height: 30px;
	margin-top:8px;
	color: #2196F3;
}

.switcher-item {
	cursor: pointer;
	text-decoration: none;
	display: inline-block;
	padding: 6px 4px;
	font-size: 18px;
	color: #262b3e;
	background-color: transparent;
	margin-right: 8px;
	border: none;
	border-radius: 4px;
	outline: none;
}

.switcher-item:hover {
	background-color: #f2f3f5;
}

.switcher-active-item {
	text-decoration: none;
	cursor: default;
	color: #262b3e;
}

.switcher-active-item,
.switcher-active-item:hover {
	background-color: #e1eff9;
}

    </style>`;

document.head.insertAdjacentHTML("beforeend", switcher_css);

var switcherElement = document.createElement('div');
switcherElement.classList.add('switcher');

function createSimpleSwitcher(items, activeItem, activeItemChangedCallback) {
    var options = activeItem;
	var intervalElements = items.map(function(item) {
		var itemEl = document.createElement('button');
		itemEl.innerText = item;
		itemEl.classList.add('switcher-item');
		itemEl.classList.toggle('switcher-active-item', item === activeItem);
		itemEl.addEventListener('click', function() {
			onItemClicked(item);
		});
		switcherElement.appendChild(itemEl);
		return itemEl;
	});

	function onItemClicked(item) {
		if (item === activeItem && options != "normalButton") {
			return;
		}

		intervalElements.forEach(function(element, index) {
			element.classList.toggle('switcher-active-item', items[index] === item);
		});

		activeItem = item;

		activeItemChangedCallback(item);
	}

	return intervalElements;
}

//var intervals = ['1mo','3mo','6mo', '1y', '2y', '5y', 'max'];
var intervals = /*enough see mo in y*/['1y', '2y', '5y', 'max'];
//                                      by default, it is '2y'
//  intervals Switch
var ivSW = createSimpleSwitcher(intervals, '2y', (item) => {
    console.log('switch to ', item);
    sendwq('intervals', item); // e.id = 'switcher' and e.data = item
});
console.log("ivSW", ivSW);
// PrintScreeN
var extras = ['Psn', 'PT', 'TR'];
var exSW = createSimpleSwitcher(extras, 'normalButton', (item) => {
    console.log('switch to ', item);
    sendwq('extra', item);
});

document.body.appendChild(switcherElement);
