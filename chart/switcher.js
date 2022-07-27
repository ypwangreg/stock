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
	padding: 6px 8px;
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

function createSimpleSwitcher(items, activeItem, activeItemChangedCallback) {
	var switcherElement = document.createElement('div');
	switcherElement.classList.add('switcher');

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
		if (item === activeItem) {
			return;
		}

		intervalElements.forEach(function(element, index) {
			element.classList.toggle('switcher-active-item', items[index] === item);
		});

		activeItem = item;

		activeItemChangedCallback(item);
	}

	return switcherElement;
}

var intervals = ['1mo','3mo','6mo', '1y', '2y', '5y', 'max'];
//                                               by default, it is '2y'
var switcherElement = createSimpleSwitcher(intervals, intervals[4], (item) => {
    console.log('switch to ', item);
    sendwq('switcher', item); // e.id = 'switcher' and e.data = item
});
document.body.appendChild(switcherElement);
