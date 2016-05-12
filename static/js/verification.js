//表单验证是否为空
function checkNull()
{
     var num=0;
     var str="";
     $("input[type$='number']").each(function(n){
          if($(this).val()=="")
          {
               num++;
               str+="您好！"+$(this).attr("msg")+"至少发一个！\r\n";
          }
     });
     if(num>0)
     {
          alert(str);
          return false;
     }
     else
     {
          return true;
     }
}