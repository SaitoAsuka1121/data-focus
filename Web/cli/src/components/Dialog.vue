<template>
	<div class="dialogform">
		<div>
			<el-button type="primary" @click="Visible = true" size="mini"
				>添加表</el-button
			>
		</div>
		<el-dialog
			title="数据选择"
			v-model="Visible"
			style="height: 15%;"
			width="40%"
			custom-class="updata"
		>
			<el-container>
				<el-header>
					<div>
						<el-radio-group v-model="radio_type" size="medium">
							<el-radio-button
								v-for="item in typeitems"
								:label="item.label"
								:key="item.value"
								>{{ item.label }}</el-radio-button
							>
						</el-radio-group>
						<div v-show="radio_type == '数据库集'">
							<el-form
								:model="databaseSet"
								:inline="false"
								title="选择数据"
								ref="databaseSet"
							>
								<el-form-item prop="name" label="数据表名">
									<el-input v-model="databaseSet.name"></el-input>
								</el-form-item>
								<el-form-item prop="databaseName" label="数据库选择">
									<div class="select">
										<el-select
											v-model="databaseSet.databaseName"
											placeholder="请选择"
											@change="currentSel"
										>
											<el-option
												v-for="item in database_list"
												:key="item.display_name"
												:label="item.display_name"
												:value="item.sqlalchemy_uri"
											>
											</el-option>
										</el-select>
									</div>
								</el-form-item>
								<el-form-item porp="databaseTablename" label="数据表选择">
									<div class="select">
										<el-select
											v-model="databaseSet.databaseTablename"
											placeholder="请选择"
										>
											<el-option
												v-for="item in table_list"
												:key="item.display_name"
												:label="item.display_name"
												:value="item.display_name"
											>
											</el-option>
										</el-select>
									</div>
								</el-form-item>
							</el-form>
							<br />
						</div>
						<div v-show="radio_type == 'Excel/CSV数据集'" class="excelcsv">
							<upfile />
						</div>
					</div>
				</el-header>
				<el-main> </el-main>
			</el-container>
			<template #footer>
				<div v-show="radio_type == '数据库集'">
					<span class="dialog-footer">
						<el-button @click="Visible = false">取 消</el-button>
						<el-button type="primary" @click="onsubmit('databaseSet')"
							>确 定</el-button
						>
					</span>
				</div>
				<div v-show="radio_type == 'Excel数据集'">
					<div class="upfile">
						<upfile />
					</div>
				</div>
			</template>
		</el-dialog>
	</div>
</template>
<script>
import Upfile from './Upfile.vue';
export default {
	components: { Upfile },
	data() {
		return {
			Visible: false,
			radio_type: '数据库集',
			typeitems: [
				{ label: '数据库集', value: 1 },
				{ label: 'Excel/CSV数据集', value: 2 }
			],
			databaseSet: {
				name: '',
				databaseName: '',
				databaseTablename: '',
				file: ''
			},
			excSet: {
				table_name: '',
				databaseName: ''
			},
			database_list: [],
			table_list: []
		};
	},
	created() {
		this.$axios.get('/database/list').then(res => {
			this.database_list = res.data.database_list;
		});
	},
	methods: {
		currentSel() {
			let data = { sqlalchemy_uri: this.databaseSet.databaseName };
			this.$axios.post('/database/get_tables', data).then(res => {
				this.table_list = res.data.table_list;
			});
		},
		onsubmit(databaseSet) {
			this.$refs[databaseSet].validate(valid => {
				if (valid) {
					let { name, databaseName, databaseTablename } = this.databaseSet;
					let data = {
						name: name,
						source: databaseName,
						databaseTablename: databaseTablename
					};
					this.$axios.post('/database/add_table', data).then(res => {
						console.log(res);
						if (res.data.code === 0) {
							this.$message({
								message: '添加成功',
								type: 'success'
							});
							location.reload()
						} else {
							this.$message({
								message: res.data.message,
								type: 'error'
							});
						}
					});
				}
			});
		},
		uploadUrl: function() {
			return 'http://localhost:5000/database/upload'; //接口
		},
		//文件上传成功触发
		uploadSuccess(response) {
			if (response.code == 0) {
				this.$message({
					message: '导入成功',
					type: 'success'
				});
				location.reload()
			} else {
				this.$message({
					message: '导入失败',
					type: 'error'
				});
			}
		},
		//文件上传失败触发
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
			const extension3 = file.name.split('.')[1] === 'txt';
			if (!extension && !extension2 && !extension3) {
				this.$message({
					message: '上传文件只能是 xls、xlsx、txt 格式!',
					type: 'error'
				});
			}
			return extension || extension2 || extension3;
		},
		//表单提交
		submitUpload() {
			this.$refs.upload.submit();
		}
	}
};
</script>
<style lang="less" scoped>
/deep/ .updata {
	height: 32.5rem;
	border-radius: 2%;
	box-shadow: 1px 1px 5px black;
}
.select {
	// background-color: red;
	position: relative;
	left: -0rem;
}
.dialog-footer {
	// background-color: red;
	position: relative;
	left: -15rem;
	top: 12rem;
}
</style>
