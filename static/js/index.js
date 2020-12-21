$(function () {

    var text2;//获取后端得到的值
    var a;//作为是否输出语句的控制条件
    var text;//

    $("#btn").click(function () {

         a=$("input[name = a]").val();
         console.log(a);//了解a是否获值成功

         var data2={};//用于作为数据被传输
         data2['name']=$('#a').val();
         console.log(data2.name);//了解data2是否获值成功

         text = document.getElementById("a");

    //用户输入不为空，页面显示用户的值
        if (text.value == "")
        {
            alert("发送信息为空，请输入！")
        }
        else
        {
            var user="default"
            //alert(text.value)
            AddMsg(user, SendMsgDispose(text.value));
            text.value = "";
        }

    //ajax提交
    $.ajax({
        type:'post',
        url:'/text',
        data:data2,
        dataType:'json',
        success:function (data) {

                console.log(data.result)

    //用户输入不为空，页面显示后台传来的的值
            if(a!="")//若用户端有输入则不需要输出
            {
                text2 = data.result;
                //alert(data.result)
                // alert(text2)
                var user2="nodefault";

                Creaduser(user2);
                // alert(data.result)
            }
        }
    })
    })

    //页面显示调用函数
    function Creaduser(user){
        //alert(text2)
        AddMsg(user, SendMsgDispose(text2));
        text2= "";
    }
    //发送消息
    function  SendMsgDispose(detail){
        detail = detail.replace("\n", "<br>").replace(" ", " ")
        return detail;
    }

    //增加信息
    function AddMsg(user,content){
        var str = CreadMsg(user,content);
        var msgs = document.getElementById("msgs");
            msgs.innerHTML = msgs.innerHTML + str;
            page_init();
    }

    //生成内容
    function CreadMsg(user,content){
          var str = "";
          var add = "您是想问："
         if(user == 'default')//user=default,输出用户输入的值
         {
             str = "<div class=\"c-right\">"+content+"<img src=\"../static/images/Tourist.png\" alt=\"jimi智能客服\" width=\"50\" height=\"50\"/></div>"
         }
         else//user=default,输出后台返回的值
         {
             str = "<div class=\"c-left\"><img src=\"../static/images/jimi.png\" alt=\"jimi智能客服\" width=\"50\" height=\"50\"/>"+add+content+"</div>";
          }

         return str;
    }
    //滚动栏时刻在最底部
    function page_init(){
        var div = document.getElementById('msgs');
        div.scrollTop = div.scrollHeight;
         }
    })