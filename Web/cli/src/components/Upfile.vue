<template>
	<el-form
		ref="form"
		label-position="left"
		:model="form"
		:rules="rules"
		label-width="80px"
		
	>
		<el-form-item label="表名" prop="display_name">
			<el-input v-model="form.display_name"></el-input>
		</el-form-item>
		<el-form-item label="数据库" prop="sqlalchemy_uri">
			<el-select v-model="form.sqlalchemy_uri" placeholder="请选择">
				<el-option
					v-for="item in database_list"
					:key="item.display_name"
					:label="item.display_name"
					:value="item.sqlalchemy_uri"
				>
				</el-option>
			</el-select>
		</el-form-item>
		<el-form-item label="上传文件" prop="excelFile">
			<div class="myupclass">
				<el-upload
					ref="upload"
					:action="uploadUrl()"
					name="excelFile"
					drag
					:data="upData"
					:with-credentials="true"
					:file-list="fileList"
					:on-error="uploadFalse"
					:on-success="uploadSuccess"
					:auto-upload="false"
					:before-upload="beforeAvatarUpload"
				>
					<i class="el-icon-upload"></i>
					<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
				</el-upload>
			</div>
		</el-form-item>

		<el-form-item>
			<div class="button">
				<el-button type="primary" @click="submitUpload(form)" v-loading.fullscreen.lock="fullscreenLoading"> 导入</el-button>
				<el-button @click="onCancel(form)">取消</el-button>
			</div>
		</el-form-item>
	</el-form>
</template>

<script>
export default {
	data() {
		return {
			rules: {
				coordinateType: [
					{
						required: true,
						message: '请选择文件中的坐标类型',
						trigger: 'change'
					}
				]
			},
			form: {
				fileName: '',
				sqlalchemy_uri: '',
				display_name: ''
			},
			fileList: [],
			database_list: [],
			fullscreenLoading: false,
		};
	},
	computed: {
		// 这里定义上传文件时携带的参数，即表单数据
		upData: function() {
			return this.form;
		}
	},
	created() {
		this.$axios.get('/database/list').then(res => {
			this.database_list = res.data.database_list;
			console.log(this.database_list);
		});
	},
	methods: {
		//导入接口地址
		uploadUrl: function() {
			return 'http://dreamstartcloud.top:5000/database/upload'; //接口
		},
		//文件上传成功触发
		uploadSuccess(response) {
			console.log(response);
			if (response.code == 0) {
				this.fullscreenLoading=false;
				this.$message({
					message: '导入成功',
					type: 'success'
				});
				location.reload();
			} else {
				this.$message({
					message: '导入失败',
					type: 'error'
				});
			}
		},
		
		uploadFalse() {
			this.$message({
				message: '文件上传失败！',
				type: 'error'
			});
		},
		// 上传前对文件的大小和类型的判断
		beforeAvatarUpload(file) {
			this.form.fileName = file.name;
			const extension = file.name.split('.')[1] === 'xls';
			const extension2 = file.name.split('.')[1] === 'xlsx';
			const extension3 = file.name.split('.')[1] === 'csv';
			if (!extension && !extension2 && !extension3) {
				this.$message({
					message: '上传文件只能是 xls、xlsx、csv 格式!',
					type: 'error'
				});
			}
			return extension || extension2 || extension3;
		},
		//表单提交
		submitUpload() {
			this.fullscreenLoading=true;
			this.$refs.form.validate(valid => {
				if (valid) {
					//触发组件的action
					this.$refs.upload.submit();
				} else {
					console.log('error submit!!');
					return false;
				}
			});
		},
		//表单取消
		onCancel() {
			this.$refs.form.resetFields();
		}
	}
};
</script>
<style lang="less" scoped>
.button{
	// background-color: red;
	position: relative;
	top: -1.25rem;
	left: -1.875rem;
}
</style>
