<template>
	<Split v-model="this_split">
		<div slot="left">
			<slot name="left"></slot>
		</div>
		<div slot="trigger">
			<div>
				<span class="dot"></span>
				<span class="dot"></span>
				<span class="dot"></span>
				<span class="dot"></span>
				<span class="dot"></span>
			</div>
		</div>
		<div slot="right">
			<slot name="right"></slot>
		</div>
	</Split>
</template>
<script>
	export default {
		data() {
			return {
				this_split: 0.5
			}
		},
		created() {
			this.this_split = this.split
		},
		props: {
			split: {
				type: Number,
			}
		}
	}
</script>
<style>

</style>