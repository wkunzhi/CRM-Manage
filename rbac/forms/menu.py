# create: '2018/12/18' - 362416272@qq.com  
from django import forms
from django.utils.safestring import mark_safe
from rbac import models

from rbac.forms.base import BootStrapModelForm

# 通过 根目录下 GetFont.py 采集到的最新版图标库
read_list = ['medkit', 'square-o', 'search-plus', 'arrows-v', 'code', 'eye', 'location-arrow', 'cubes', 'user-plus', 'hand-o-down', 'institution', 'scribd', 'battery-three-quarters', 'snapchat-ghost', 'foursquare', 'sort-alpha-asc', 'cc-stripe', 'desktop', 'caret-left', 'star', 'sort-asc', 'exchange', 'mouse-pointer', 'qrcode', 'chevron-circle-up', 'gavel', 'arrow-up', 'share-square', 'first-order', 'file-zip-o', 'camera-retro', 'caret-up', 'whatsapp', 'battery', 'venus-mars', 'forumbee', 'star-half-empty', 'behance-square', 'space-shuttle', 'file-image-o', 'lastfm-square', 'codiepie', 'user-times', 'won', 'ellipsis-v', 'viacoin', 'rub', 'exclamation-circle', 'step-backward', 'gg', 'trash', 'reddit-square', 'battery-quarter', 'exclamation-triangle', 'map-pin', 'hard-of-hearing', 'soundcloud', 'link', 'vimeo-square', 'credit-card', 'navicon', 'telegram', 'hand-stop-o', 'upload', 'tumblr', 'ban', 'folder-o', 'thermometer-3', 'play-circle-o', 'bus', 'caret-square-o-down', 'thermometer-empty', 'save', 'chevron-circle-right', 'newspaper-o', 'hand-lizard-o', 'bolt', 'paint-brush', 'legal', 'envira', 'stumbleupon-circle', 'low-vision', 'mail-reply-all', 'plane', 'tag', 'users', 'eye-slash', 'check-square-o', 'sort-amount-desc', 'gitlab', 'maxcdn', 'wpforms', 'jsfiddle', 'leaf', 'envelope-square', 'industry', 'steam', 'connectdevelop', 'list-ol', 'bed', 'feed', 'resistance', 'step-forward', 'google-plus', 'shopping-basket', 'unsorted', 'facebook-official', 'toggle-down', 'stop', 'plus-square-o', 'archive', 'bathtub', 'modx', 'phone-square', 'reply', 'support', 'angle-up', 'eject', 'image', 'yc-square', 'child', 'object-group', 'arrows-h', 'level-down', 'linkedin-square', 'random', 'rouble', 'superscript', 'camera', 'neuter', 'pencil', 'pause-circle-o', 'check-square', 'chain-broken', 'unlink', 'wheelchair-alt', 'gear', 'stop-circle', 'calendar-times-o', 'comment', 'cc-mastercard', 'venus', 'circle', 'bullhorn', 'snapchat-square', 'copy', 'heart', 'deviantart', 'gears', 'linkedin', 'medium', 'rebel', 'futbol-o', 'odnoklassniki', 'th', 'forward', 'search', 'intersex', 'calendar-minus-o', 'bluetooth', 'etsy', 'area-chart', 'sort-down', 'user', 'retweet', 'flickr', 'twitch', 'spoon', 'minus-square', 'thermometer-4', 'sheqel', 'automobile', 'times-rectangle-o', 'tablet', 'minus-circle', 'google', 'lemon-o', 'arrow-down', 'fonticons', 'sort-desc', 'openid', 'adn', 'file-text-o', 'hourglass-1', 'envelope-open', 'gratipay', 'university', 'suitcase', 'toggle-on', 'caret-square-o-right', 'skyatlas', 'birthday-cake', 'star-half', 'ravelry', 'stack-exchange', 'train', 'envelope', 'cloud', 'meh-o', 'drivers-license', 'send', 'file-o', 'puzzle-piece', 'eyedropper', 'pied-piper-alt', 'cart-plus', 'tencent-weibo', 'wikipedia-w', 'list-ul', 'thumbs-o-down', 'rss-square', 'pied-piper', 'caret-right', 'hand-paper-o', 'clone', 'address-card', 'sign-language', 'volume-up', 'font', 'arrows', 'repeat', 'shopping-bag', 'text-height', 'user-circle-o', 'edit', 'times-circle', 'bar-chart-o', 'dedent', 'laptop', 'window-close-o', 'street-view', 'bell-slash', 'code-fork', 'bomb', 'address-book', 'filter', 'hand-peace-o', 'opera', 'genderless', 'unlock-alt', 'fast-forward', 'battery-3', 'h-square', 'motorcycle', 'buysellads', 'shirtsinbulk', 'hand-o-right', 'exclamation', 'times', 'yahoo', 'sort-up', 'bars', 'diamond', 'mortar-board', 'stack-overflow', 'flash', 'pinterest', 'ticket', 'microchip', 'quora', 'tripadvisor', 'window-close', 'cc', 'life-saver', 'paper-plane-o', 'lastfm', 'battery-2', 'hashtag', 'arrow-left', 'volume-control-phone', 'thermometer-2', 'simplybuilt', 'gbp', 'fast-backward', 'calculator', 'user-secret', 'address-card-o', 'book', 'rss', 'beer', 'bar-chart', 'hacker-news', 'hand-scissors-o', 'database', 'trophy', 'pied-piper-pp', 'sliders', 'hand-grab-o', 'television', 'picture-o', 'y-combinator-square', 'life-bouy', 'folder-open-o', 'weibo', 'download', 'caret-square-o-up', 'xing', 'angle-down', 'youtube', 'codepen', 'cc-amex', 'question-circle-o', 'wechat', 'file-powerpoint-o', 'rotate-left', 'id-card-o', 'window-minimize', 'map-o', 'align-right', 'search-minus', 'flag', 'eercast', 'at', 'phone', 'user-o', 'fax', 'snowflake-o', 'hotel', 'smile-o', 'barcode', 'instagram', 'percent', 'ioxhost', 'align-justify', 'user-circle', 'arrow-circle-o-right', 'long-arrow-up', 'flag-checkered', 'lock', 'battery-full', 'github-square', 'audio-description', 'clipboard', 'indent', 'hand-pointer-o', 'bell', 'usd', 'dot-circle-o', 'thermometer-0', 'glide', 'facebook-square', 'vcard', 'caret-square-o-left', 'sort-alpha-desc', 'share', 'long-arrow-right', 'facebook-f', 'times-rectangle', 'hospital-o', 'key', 'shower', 'map-signs', 'trash-o', 'fighter-jet', 'digg', 'ellipsis-h', 'sun-o', 'reorder', 'remove', 'facebook', 'stumbleupon', 'fort-awesome', 'thumb-tack', 'file-code-o', 'registered', 'delicious', 'venus-double', 'pagelines', 'wifi', 'skype', 'slack', 'assistive-listening-systems', 'drivers-license-o', 'turkish-lira', 'deafness', 'qq', 'id-badge', 'music', 'folder-open', 'joomla', 'clock-o', 'sort-numeric-asc', 'american-sign-language-interpreting', 'volume-off', 'meanpath', 'group', 'taxi', 'print', 'github', 'unlock', 'arrow-circle-o-down', 'grav', 'ils', 'dropbox', 'toggle-left', 'thumbs-down', 'mars-double', 'window-maximize', 'mail-forward', 'send-o', 'th-list', 'tasks', 'try', 'signing', 'bold', 'rmb', 'chain', 'hand-spock-o', 'edge', 'headphones', 'table', 'reply-all', 'hourglass-start', 'scissors', 'battery-0', 'arrow-circle-right', 'ruble', 'rocket', 'xing-square', 'building', 'tumblr-square', 'android', 'home', 'compass', 'mars-stroke-v', 'files-o', 'plus-square', 'euro', 'cog', 'linode', 'hourglass-end', 'behance', 'long-arrow-down', 'times-circle-o', 'twitter', 'thermometer-full', 'viadeo', 'pause-circle', 'yelp', 'html5', 'pencil-square-o', 'th-large', 'leanpub', 'bitbucket', 'hourglass-o', 'paper-plane', 'commenting', 'shopping-cart', 'external-link-square', 'ambulance', 'y-combinator', 'creative-commons', 'crosshairs', 'ra', 'windows', 'paypal', 'spotify', 'envelope-o', 'bitbucket-square', 'signal', 'subway', 'usb', 'heartbeat', 'pencil-square', 'soccer-ball-o', 'cny', 'magic', 'quote-left', 'google-plus-square', 'angle-right', 'wheelchair', 'user-md', 'columns', 'crop', 'italic', 'opencart', 'ge', 'sign-out', 'github-alt', 'align-center', 'mars-stroke-h', 'thermometer-quarter', 'check-circle-o', 'sort', 'toggle-off', 'eraser', 'header', 'themeisle', 'mobile', 'tv', 'chevron-left', 'graduation-cap', 'photo', 'battery-empty', 'comments', 'imdb', 'magnet', 'sort-amount-asc', 'chevron-down', 'glide-g', 'wordpress', 'hourglass-3', 'apple', 'map', 'yc', 'calendar-o', 'eur', 'life-buoy', 'won fa-fw', 'superpowers', 'backward', 'lightbulb-o', 'file-video-o', 'sitemap', 'bicycle', 'google-wallet', 'text-width', 'google-plus-official', 'strikethrough', 'paw', 'balance-scale', 'anchor', 'sticky-note', 'calendar-plus-o', 'vcard-o', 'optin-monster', 'bitcoin', 'thumbs-up', 'window-restore', 'product-hunt', 'yen', 'rupee', 'yoast', 'handshake-o', 'object-ungroup', 'transgender', 'language', 'battery-4', 'mercury', 'comment-o', 'star-half-full', 'arrow-circle-up', 'podcast', 'hand-o-up', 'flag-o', 'reddit-alien', 'bank', 'map-marker', 'mixcloud', 'paragraph', 'cab', 'battery-1', 'internet-explorer', 'youtube-square', 'bell-slash-o', 'life-ring', 'outdent', 'microphone', 'free-code-camp', 'level-up', 'stop-circle-o', 'coffee', 'floppy-o', 'chevron-up', 'align-left', 'plug', 'question-circle', 'dashboard', 'toggle-right', 'wpbeginner', 'battery-half', 'cloud-upload', 'trademark', 'heart-o', 'black-tie', 'btc', 'long-arrow-left', 'thermometer-1', 'file-excel-o', 'folder', 'file-picture-o', 'arrows-alt', 'shield', 'film', 'frown-o', 'reddit', 'asl-interpreting', 'angle-double-down', 'braille', 'hdd-o', 'tty', 'file-text', 'quote-right', 'jpy', 'dribbble', 'vimeo', 'car', 'vine', 'bath', 'sort-numeric-desc', 'cart-arrow-down', 'line-chart', 'commenting-o', 'plus-circle', 'pinterest-square', 'share-alt-square', 'chevron-circle-left', 'share-alt', 'list', 'pause', 'sign-in', 'globe', 'hourglass', 'youtube-play', 'cc-paypal', 'share-square-o', 'envelope-open-o', 'check', 'cut', 'info-circle', 'adjust', 'mobile-phone', 'rotate-right', 'hourglass-half', 'file-movie-o', 'inbox', 'inr', 'subscript', 'play', 'expeditedssl', 'list-alt', 'expand', 'id-card', 'bluetooth-b', 'briefcase', 'wpexplorer', 'fire-extinguisher', 'minus-square-o', 'css3', 'sellsy', 'tree', 'calendar', 'wrench', 'gift', 'play-circle', 'dollar', 'mail-reply', 'binoculars', 'drupal', 'warning', 'moon-o', 'file-photo-o', 'caret-down', 'thermometer-three-quarters', 'bookmark', 'google-plus-circle', 'ship', 'git', 'umbrella', 'fa', 'stethoscope', 'pie-chart', 'volume-down', 'compress', 'thermometer', 'chevron-right', 'bullseye', 'glass', 'shekel', 'cube', 'arrow-circle-left', 'linux', 'bandcamp', 'square', 'paperclip', 'contao', 'angellist', 'file-pdf-o', 'krw', 'cc-visa', 'arrow-right', 'plus', 'get-pocket', 'arrow-circle-o-up', 'bell-o', '500px', 'amazon', 'circle-o', 'underline', 'gittip', 'address-book-o', 'credit-card-alt', 'truck', 'hand-o-left', 'mars-stroke', 'transgender-alt', 'gamepad', 'universal-access', 'certificate', 'cloud-download', 'file-archive-o', 'i-cursor', 'arrow-circle-down', 'bug', 'firefox', 'star-half-o', 'cc-jcb', 'renren', 'snapchat', 'fire', 'mars', 'chevron-circle-down', 'angle-double-up', 'pinterest-p', 'weixin', 'toggle-up', 'undo', 'gg-circle', 'cutlery', 'hourglass-2', 'power-off', 'file-sound-o', 'thumbs-o-up', 'external-link', 'tags', 'arrow-circle-o-left', 'history', 'dashcube', 'thermometer-half', 'male', 'money', 'check-circle', 'video-camera', 'server', 'bookmark-o', 'road', 'viadeo-square', 'circle-o-notch', 'terminal', 'flask', 'git-square', 'question', 'recycle', 'houzz', 'file', 'vk', 'meetup', 'star-o', 'angle-double-right', 'font-awesome', 'circle-thin', 'odnoklassniki-square', 'spinner', 'tachometer', 'deaf', 'cc-diners-club', 'slideshare', 'paste', 'twitter-square', 's15', 'blind', 'keyboard-o', 'hand-rock-o', 'cc-discover', 'minus', 'microphone-slash', 'tint', 'copyright', 'steam-square', 'safari', 'comments-o', 'refresh', 'asterisk', 'female', 'empire', 'info', 'calendar-check-o', 'angle-left', 'chrome', 'close', 'trello', 'angle-double-left', 'sticky-note-o', 'file-audio-o', 'file-word-o', 'building-o', 'cogs']

# 图标处理为i标签
icon_list = [['fa fa-'+icon, mark_safe('<i class="fa fa-' + icon + '" aria-hidden="true"></i>')] for icon in read_list]


class MenuModelForm(forms.ModelForm):
    """一级菜单FORM"""
    class Meta:
        model = models.Menu
        fields = ['title', 'sort', 'icon']
        # 给标签加上boot样式
        widgets = {
            'title': forms.TextInput(attrs={'class': 'layui-input'}),  # 渲染的时候添加class属性
            'sort': forms.TextInput(attrs={'class': 'layui-input'}),
            'icon': forms.RadioSelect(  # 转换成单选框 Radio
                choices=icon_list,
                attrs={'class': 'clearfix'}  # boot中清除浮动
            )
        }


class SecondMenuModelForm(BootStrapModelForm):  # 【继承事先写好的boot类直接实现添加boot样式】适用于简单的boot
    class Meta:
        model = models.Permission
        # fields = ['title', 'url', 'name', 'menu']
        exclude = ['pid']  # 等同于上面一行，只是排除掉pid不显示


class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'name', 'url']


class MultiAddPermissionForm(forms.Form):
    """批量添加"""
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'layui-input'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'layui-input'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'layui-input'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'layui-input'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'layui-input'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


class MultiEditPermissionForm(forms.Form):
    """批量修改"""
    id = forms.IntegerField(
        widget=forms.HiddenInput()  # 自动隐藏
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'layui-input'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'layui-input'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'layui-input'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'layui-input layui-unselect'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'layui-input layui-unselect'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')
