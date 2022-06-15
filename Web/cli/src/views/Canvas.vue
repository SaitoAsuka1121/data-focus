<template>
	<div class="home">
		<div class="mainNavigation" v-show="seeall == true">
			<el-container class="heightAll">
				<el-aside class="heightAll">
					<navigator />
				</el-aside>
			</el-container>
		</div>
		<el-container>
			<div class="topnav" v-show="seeall == true">
				<div class="showTime"></div>
				<div class="addcomp">
					<el-button
						icon="el-icon-circle-plus-outline"
						size="small"
						@click="onSubmit()"
						style="width: 70px;"
						>添加</el-button
					>
				</div>
				<div class="seecomp">
					<el-button
						icon="el-icon-view"
						size="small"
						@click="seeall = false"
						style="width: 100px;"
						>预览仪表板</el-button
					>
				</div>
			</div>
			<div class="topnav" v-show="seeall == false">
				<div class="savecomp">
					<el-button
						icon="el-icon-download"
						size="small"
						@click="saveImage('app', '图表')"
						style="width: 110px;"
						>另存为图片</el-button
					>
				</div>
				<div class="seecomp">
					<el-button
						icon="el-icon-view"
						size="small"
						@click="seeall = true"
						style="width: 100px;"
						>返回编辑</el-button
					>
				</div>
			</div>
			<div class="save" id="Top3Img" ref="Top3Img">
				<component
					v-for="(item, index) in counter"
					:key="index"
					:is="item.name"
					@func="getContent(index)"
					:count="index"
				></component>
			</div>
		</el-container>
	</div>
</template>
<script>
import html2canvas from 'html2canvas';
import Chart from '../components/Chart.vue';
import Navigator from '../components/Navigator.vue';
export default {
	name: 'Canvas',
	components: {
		Navigator,
		Chart
	},
	data() {
		return {
			counter: [],
			count: 0,
			seeall: true
		};
	},
	mounted() {
		var t = null;
		t = setTimeout(time, 1000);
		function time() {
			clearTimeout(t);
			let dt = new Date();
			var y = dt.getFullYear();
			var mt = dt.getMonth() + 1;
			var day = dt.getDate();
			var h = dt.getHours();
			var m = dt.getMinutes();
			var s = dt.getSeconds();
			document.querySelector('.showTime').innerHTML =
				'当前时间：' +
				y +
				'年' +
				mt +
				'月' +
				day +
				'日' +
				h +
				'时' +
				m +
				'分' +
				s +
				'秒';
			t = setTimeout(time,1000);
		}
	},
	methods: {
		onSubmit() {
			this.counter.push({
				name: 'Chart'
			});
			this.count++;
		},
		getContent(index) {
			console.log(index);
			this.counter.splice(index, 1);
			console.log(this.counter);
		},
		dataURLToBlob(dataurl) {
            let arr = dataurl.split(',');
            let mime = arr[0].match(/:(.*?);/)[1];
            let bstr = atob(arr[1]);
            let n = bstr.length;
            let u8arr = new Uint8Array(n);
            while (n--) {
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new Blob([u8arr], { type: mime });
        },
        /*保存图片的方法（即按钮点击触发的方法）
          第一个参数为需要保存的div的id名
          第二个参数为保存图片的名称 */
        saveImage(divText, imgText) {
            let canvasID = this.$refs[divText];
            let that = this;
			console.log(canvasID);
            let a = document.createElement('a');
            html2canvas(document.body).then(canvas => {
                let dom = document.body.appendChild(canvas);
                dom.style.display = 'none';
                a.style.display = 'none';
                document.body.removeChild(dom);
                let blob = that.dataURLToBlob(dom.toDataURL('image/png'));
                a.setAttribute('href', URL.createObjectURL(blob));
                //这块是保存图片操作  可以设置保存的图片的信息
                a.setAttribute('download', imgText + '.png');
                document.body.appendChild(a);
                a.click();
                URL.revokeObjectURL(blob);
                document.body.removeChild(a);
            });
        },
		
	}
};
</script>
<style lang="less" scoped>
* {
	margin: 0;
	padding: 0;
}
.topnav {
	background-color: white;
	width: 100%;
	height: 2.5rem;
	max-width: 192.875rem;
	min-width: 64rem;
	box-shadow: 1px 1px 10px #909090;
	border-bottom: 1px solid rgba(0, 0, 200, 0.4);
	.showTime {
		position: relative;
		font-size: 1.25rem;
		left: 37.5rem;
		width: 25rem;
		height: 2.5rem;
		top: 6px;
		// background-color: red;
	}
	.addcomp {
		position: absolute;
		left: 5rem;
		top: -2px;
		margin-top: 0.3125rem;
	}
	.seecomp {
		position: absolute;
		right: 0.625rem;
		top: 0.3125rem;
	}
	.savecomp {
		position: relative;
		left: -43.75rem;
		top: 3px;
		// background-color: red;
	}
}
.save {
	width: 1px;
	height: 1px;
}
</style>
