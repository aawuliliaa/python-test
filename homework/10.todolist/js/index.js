//添加到运行中的列表
function addToRunning() {
    //获取input标签js对象
    let addToRunningTag = document.getElementById('addToRunning');
    //获取input标签中的内容
    let tagValue = addToRunningTag.value;
    //获取正在进行中的li标签
    let runningListTag = document.getElementById('runningList');
    let p_guid = guid();
    //创建新的li标签
    let new_li_tag = createLiItem(tagValue,p_guid);
    //添加到正在进行中的列表中
    runningListTag.appendChild(new_li_tag);
    let local_storage_data = load_list_item();
    //添加新的数据到local_storage中
    //{'3123':{"pTagValue":tagValue,"isRunning":true}}"isRunning":true用于设置是在运行中还是在已经完成列表
    local_storage_data[p_guid]={"pTagValue":tagValue,"isRunning":true};
    local_storage_data["runningListCount"] += 1;
    //保存到浏览器中，用于刷新浏览器或重新加载浏览器，展示数据使用
    saveToLocalStorage(local_storage_data);
    //把运行中的数目加1，展示到页面中
    let runningCountTag = document.getElementById('runningCount');
    runningCountTag.innerText=local_storage_data["runningListCount"];
    addToRunningTag.value="";
}

//创建一个下面的标签
//创建新的li标签
// <li  class="list-item">
//     <input type="checkbox" onchange="move()">
//     <p onclick="edit()" id="">1111</p>
//     <a href="javascript:remove()">-</a>
// </li>
function createLiItem(p_innerText,p_guid) {
    //设置父标签li
    let li_tag = document.createElement('li');
    li_tag.setAttribute('class','list-item');
    li_tag.setAttribute('id',`li-${p_guid}`);
    //设置input标签并设置属性
    let input_tag = document.createElement('input');
    input_tag.setAttribute('type','checkbox');
    input_tag.setAttribute('onchange',`move('${p_guid}')`);
    //设置P标签并设置属性
    let p_tag = document.createElement('p');
    p_tag.setAttribute('onclick',`edit('${p_guid}')`);
    p_tag.setAttribute('id',p_guid);
    p_tag.innerText=p_innerText;
    //设置a标签，并设置属性
    let a_tag = document.createElement('a');
    a_tag.setAttribute('href',`javascript:remove('${p_guid}')`);
    a_tag.innerText='-';
    //把新创建的字标签添加到父标签li中
    li_tag.appendChild(input_tag);
    li_tag.appendChild(p_tag);
    li_tag.appendChild(a_tag);
    //返回li标签对象
    return li_tag;
}

//生成uuid,用于设置新加的li的id,保证id的唯一
function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = Math.random()*16|0, v = c === 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}
//加载localStorage中的数据
function load_list_item() {
    let list_item = localStorage.getItem('list_item');
    if(list_item != null){
        return JSON.parse(list_item);
    }else{
        return {"runningListCount":0,"doneListCount":0};
    }
}
//保存数据到localStorage中
//保存到浏览器中，用于刷新浏览器或重新加载浏览器，展示数据使用
function saveToLocalStorage(data) {
    localStorage.setItem("list_item", JSON.stringify(data));
}
//删除标签
function remove(li_id) {

    let runningList = document.getElementById('runningList');
    let doneList = document.getElementById('doneList');
    let li_removed_tag = document.getElementById(`li-${li_id}`);
    //从loadStorage中获取数据
    let list_item = load_list_item();
    //在页面中，把选中的项移除掉
    if(list_item[li_id]["isRunning"]){
        runningList.removeChild(li_removed_tag);
        list_item['runningListCount']-=1;
    }else{
        doneList.removeChild(li_removed_tag);
        list_item['doneListCount']-=1;
    }
    //在localStorage中删除选中的项
    delete list_item[li_id];
    saveToLocalStorage(list_item);
    //列出运行中和完成的数目
    showListCount();
}
//移动，进行中====已经完成  互相移动
function move(li_id) {
    let runningList = document.getElementById('runningList');
    let doneList = document.getElementById('doneList');
    let li_moved_tag = document.getElementById(`li-${li_id}`);
    //从loadStorage中获取数据
    let list_item = load_list_item();
    //进行标签移除设置
    if(list_item[li_id]["isRunning"]){
        //这是从运行中移入到已经完成
        list_item[li_id]["isRunning"]=false;
        doneList.appendChild(li_moved_tag);
        list_item['runningListCount']-=1;
        list_item['doneListCount']+=1;
    }else{
        //这是从已经完成移入到正在进行
        list_item[li_id]["isRunning"]=true;
        runningList.appendChild(li_moved_tag);
        list_item['doneListCount']-=1;
        list_item['runningListCount']+=1;
    }
    saveToLocalStorage(list_item);
    //列出运行中和完成的数目
    showListCount();
}
//编辑列表中的内容
function edit(p_id) {
    //加载localStorage中的数据
    let list_item = load_list_item();
    let p_tag = document.getElementById(p_id);
    let p_tag_inner_text=p_tag.innerText;
    //我也使用一次innerHTML创建标签
    p_tag.innerHTML=`<input type="text" id="edit-${p_id}">`;
    //新加一个编辑标签，是input标签
    let edit_input_tag = document.getElementById(`edit-${p_id}`);
    //设置input标签中的默认内容
    edit_input_tag.value=p_tag_inner_text;
    //获得焦点
    edit_input_tag.focus();
    //失去焦点时的事件
    edit_input_tag.onblur = function () {
        if (edit_input_tag.value.length===0){
            alert("你什么都没有输入呀，忘记了吧！");
        }else{
            list_item[p_id]["pTagValue"]=edit_input_tag.value;
            //移除刚刚新加的input标签
            p_tag.removeChild(edit_input_tag);
            //设置好新编辑的内容
            p_tag.innerHTML = edit_input_tag.value;
            //保存到localStorage中
            saveToLocalStorage(list_item);
        }
    }
}
//列出运行中和完成的数目
function showListCount() {
    //展示已经完成的数据和正在运行中的数目
    let local_storage_data = load_list_item();
    let runningCountTag = document.getElementById('runningCount');
    runningCountTag.innerText=local_storage_data["runningListCount"];
    let doneCountTag = document.getElementById('doneCount');
    doneCountTag.innerText = local_storage_data["doneListCount"];
}
//页面重新加载时，调用的方法
function load() {
    let list_item = load_list_item();
    let runningList = document.getElementById('runningList');
    let doneList = document.getElementById('doneList');
    for (let item_id in list_item){
        if (list_item.hasOwnProperty(item_id)){
            //list_item = {'3123':{"pTagValue":tagValue,"isRunning":true}}"
            let item = createLiItem(list_item[item_id]["pTagValue"],item_id);
            //添加到运行中列表中
            if(list_item[item_id]["isRunning"]){
                runningList.appendChild(item);
                //添加到已经完成的列表中
            }else if(list_item[item_id]["isRunning"] === false) {
                item.firstChild.checked=true;
                doneList.appendChild(item);
            }
        }

    }
    showListCount();
}

//最底层的clear按钮,清除所有列表中的项
function clear() {
    let list_item = load_list_item();
    let runningList = document.getElementById('runningList');
    let doneList = document.getElementById('doneList');
    for (let item_id in list_item){
        if (list_item.hasOwnProperty(item_id)){

            let li_cleared_tag = document.getElementById(`li-${item_id}`);
            if(list_item[item_id]["isRunning"]){
                runningList.removeChild(li_cleared_tag);
            }else if(list_item[item_id]["isRunning"] === false){
                doneList.removeChild(li_cleared_tag);
            }
        }
    }
    let data={"runningListCount":0,"doneListCount":0};
    saveToLocalStorage(data);
    //列出运行中和完成的数目
    showListCount();
}

//重新刷新页面，调用load方法，展示数据
window.onload=load;
