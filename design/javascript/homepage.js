$(document)
    .ready(function() {
        var $sidebarButton = $('.attached.launch.button');

        handler = {
            menu: {
                mouseenter: function() {
                    $(this)
                        .stop()
                        .animate({
                            width: '155px'
                        }, 300, function() {
                            $(this).find('.text').show();
                        });
                },
                mouseleave: function(event) {
                    $(this).find('.text').hide();
                    $(this)
                        .stop()
                        .animate({
                            width: '70px'
                        }, 300);
                }
            },
        };

        $sidebarButton
            .on('mouseenter', handler.menu.mouseenter)
            .on('mouseleave', handler.menu.mouseleave);

        var
        changeSides = function() {
            $('.ui.shape')
                .eq(0)
                .shape('flip over')
                .end()
                .eq(1)
                .shape('flip over')
                .end()
                .eq(2)
                .shape('flip back')
                .end()
                .eq(3)
                .shape('flip back')
                .end();
        },
            validationRules = {
                Email: {
                    identifier: 'email',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入注册用的邮箱地址'
                    }, {
                        type: 'email',
                        prompt: '请输入合法的邮箱地址'
                    }]
                },
                nickName: {
                    identifier: 'nickname',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入您的昵称'
                    }]
                },
                passWord: {
                    identifier: 'password',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入密码，可包含数字，字母，特殊符号。长度在8-23个字符间'
                    }, {
                        type: 'length[8]',
                        prompt: '密码的长度需要在8-23个字符之间'
                    }]
                },
                rePassword: {
                    identifier: 'repassword',
                    rules: [{
                        type: 'match[password]',
                        prompt: '两次输入的密码不一致，请检查'
                    }]
                },
                terms: {
                    identifier: 'terms',
                    rules: [{
                        type: 'checked',
                        prompt: '需要同意这个许可'
                    }]
                }
            };

        $('.overlay.sidebar')
            .sidebar({
                overlay: true
            })
            .sidebar('toggle');

        $('.ui.checkbox')
            .checkbox();

        $('.ui.bib.modal').modal('setting', 'closable', false)
            .modal('attach events', '.blue.button', 'show');


        $('.ui.form')
            .form(validationRules, {
                inline: true,
                on: 'blur'
            });

        $('.ui.dropdown')
            .dropdown({
                on: 'hover'
            });

        $('.masthead .information')
            .transition('scale in');

        $('.ui.sidebar')
            .sidebar();
        $('.ui.sidebar').first()
            .sidebar('attach events', '.attached.launch.button');
        $('.attached.launch.button')
            .removeClass('disabled');

        setInterval(changeSides, 3000);

    });




(function($) {
    $(window).load(function() {
        $('#sti-menu').iconmenu({
            animMouseenter: {
                'mText': {
                    speed: 400,
                    easing: 'easeOutBack',
                    delay: 200,
                    dir: -1
                },
                'sText': {
                    speed: 400,
                    easing: 'easeOutBack',
                    delay: 400,
                    dir: -1
                },
                'icon': {
                    speed: 400,
                    easing: 'easeOutBack',
                    delay: 0,
                    dir: -1
                }
            },
            animMouseleave: {
                'mText': {
                    speed: 200,
                    easing: 'easeInExpo',
                    delay: 150,
                    dir: 1
                },
                'sText': {
                    speed: 200,
                    easing: 'easeInExpo',
                    delay: 300,
                    dir: 1
                },
                'icon': {
                    speed: 200,
                    easing: 'easeInExpo',
                    delay: 0,
                    dir: 1
                }
            }
        });
    });

    $(window).resize(function() {
        $('#sti-menu h2').removeAttr("style");
        $('#sti-menu h3').removeAttr("style");
        $('#sti-menu span').removeAttr("style");
        $('#sti-menu').iconmenu({
            animMouseenter: {
                'mText': {
                    speed: 400,
                    easing: 'easeOutBack',
                    delay: 200,
                    dir: -1
                },
                'sText': {
                    speed: 400,
                    easing: 'easeOutBack',
                    delay: 400,
                    dir: -1
                },
                'icon': {
                    speed: 400,
                    easing: 'easeOutBack',
                    delay: 0,
                    dir: -1
                }
            },
            animMouseleave: {
                'mText': {
                    speed: 200,
                    easing: 'easeInExpo',
                    delay: 150,
                    dir: 1
                },
                'sText': {
                    speed: 200,
                    easing: 'easeInExpo',
                    delay: 300,
                    dir: 1
                },
                'icon': {
                    speed: 200,
                    easing: 'easeInExpo',
                    delay: 0,
                    dir: 1
                }
            }
        });
    });

})(jQuery);


(function($) {

    var methods = {
        init: function(options) {

            if (this.length) {

                var settings = {
                    // configuration for the mouseenter event
                    animMouseenter: {
                        'mText': {
                            speed: 350,
                            easing: 'easeOutExpo',
                            delay: 140,
                            dir: 1
                        },
                        'sText': {
                            speed: 350,
                            easing: 'easeOutExpo',
                            delay: 0,
                            dir: 1
                        },
                        'icon': {
                            speed: 350,
                            easing: 'easeOutExpo',
                            delay: 280,
                            dir: 1
                        }
                    },
                    // configuration for the mouseleave event
                    animMouseleave: {
                        'mText': {
                            speed: 300,
                            easing: 'easeInExpo',
                            delay: 140,
                            dir: 1
                        },
                        'sText': {
                            speed: 300,
                            easing: 'easeInExpo',
                            delay: 280,
                            dir: 1
                        },
                        'icon': {
                            speed: 300,
                            easing: 'easeInExpo',
                            delay: 0,
                            dir: 1
                        }
                    },
                    // speed for the item bg color animation
                    boxAnimSpeed: 300,
                    // default text color (same defined in the css)
                    defaultTextColor: '#fff',
                    // default bg color (same defined in the css)
                    defaultBgColor: '#ccc'
                };

                return this.each(function() {

                    // if options exist, lets merge them with our default settings
                    if (options) {
                        $.extend(settings, options);
                    }

                    var $el = $(this),
                        // the menu items
                        $menuItems = $el.children('li'),
                        // save max delay time for mouseleave anim parameters
                        maxdelay = Math.max(settings.animMouseleave['mText'].speed + settings.animMouseleave['mText'].delay,
                            settings.animMouseleave['sText'].speed + settings.animMouseleave['sText'].delay,
                            settings.animMouseleave['icon'].speed + settings.animMouseleave['icon'].delay
                        ),
                        // timeout for the mouseenter event
                        // lets us move the mouse quickly over the items,
                        // without triggering the mouseenter event
                        t_mouseenter;

                    // save default top values for the moving elements:
                    // the elements that animate inside each menu item
                    $menuItems.find('.sti-item').each(function() {
                        var $el = $(this);
                        $el.data('deftop', $el.position().top);
                    });

                    // ************** Events *************
                    // mouseenter event for each menu item
                    $menuItems.bind('mouseenter', function(e) {

                        clearTimeout(t_mouseenter);

                        var $item = $(this),
                            $wrapper = $item.children('a'),
                            wrapper_h = $wrapper.height(),
                            // the elements that animate inside this menu item
                            $movingItems = $wrapper.find('.sti-item'),
                            // the color that the texts will have on hover
                            hovercolor = $item.data('hovercolor');

                        t_mouseenter = setTimeout(function() {
                            // indicates the item is on hover state
                            $item.addClass('sti-current');

                            $movingItems.each(function(i) {
                                var $item = $(this),
                                    item_sti_type = $item.data('type'),
                                    speed = settings.animMouseenter[item_sti_type].speed,
                                    easing = settings.animMouseenter[item_sti_type].easing,
                                    delay = settings.animMouseenter[item_sti_type].delay,
                                    dir = settings.animMouseenter[item_sti_type].dir,
                                    // if dir is 1 the item moves downwards
                                    // if -1 then upwards
                                    style = {
                                        'top': -dir * wrapper_h + 'px'
                                    };

                                if (item_sti_type === 'icon') {
                                    // this sets another bg image for the icon
                                    style.backgroundPosition = 'bottom left';
                                } else {
                                    style.color = hovercolor;
                                }
                                // we hide the icon, move it up or down, and then show it
                                $item.hide().css(style).show();
                                clearTimeout($item.data('time_anim'));
                                $item.data('time_anim',
                                    setTimeout(function() {
                                        // now animate each item to its default tops
                                        // each item will animate with a delay specified in the options
                                        $item
                                            .animate({
                                                top: $item.data('deftop') + 'px'
                                            }, speed, easing);
                                    }, delay)
                                );
                            });
                            // animate the bg color of the item
                            $wrapper.animate({
                                backgroundColor: settings.defaultTextColor
                            }, settings.boxAnimSpeed);

                        }, 100);

                    })
                    // mouseleave event for each menu item
                    .bind('mouseleave', function(e) {

                        clearTimeout(t_mouseenter);

                        var $item = $(this),
                            $wrapper = $item.children('a'),
                            wrapper_h = $wrapper.height(),
                            $movingItems = $wrapper.find('.sti-item');

                        if (!$item.hasClass('sti-current'))
                            return false;

                        $item.removeClass('sti-current');

                        $movingItems.each(function(i) {
                            var $item = $(this),
                                item_sti_type = $item.data('type'),
                                speed = settings.animMouseleave[item_sti_type].speed,
                                easing = settings.animMouseleave[item_sti_type].easing,
                                delay = settings.animMouseleave[item_sti_type].delay,
                                dir = settings.animMouseleave[item_sti_type].dir;

                            clearTimeout($item.data('time_anim'));

                            setTimeout(function() {

                                $item.stop(true).animate({
                                    'top': -dir * wrapper_h + 'px'
                                }, speed, easing, function() {

                                    if (delay + speed === maxdelay) {

                                        $wrapper.stop(true).animate({
                                            backgroundColor: settings.defaultBgColor
                                        }, settings.boxAnimSpeed);

                                        $movingItems.each(function(i) {
                                            var $el = $(this),
                                                style = {
                                                    'top': $el.data('deftop') + 'px'
                                                };

                                            if ($el.data('type') === 'icon') {
                                                style.backgroundPosition = 'top left';
                                            } else {
                                                style.color = settings.defaultTextColor;
                                            }

                                            $el.hide().css(style).stop(true).fadeIn();
                                        });

                                    }
                                });
                            }, delay);
                        });
                    });

                });
            }
        }
    };

    $.fn.iconmenu = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.iconmenu');
        }
    };

})(jQuery);