#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

class FilterNode : public rclcpp::Node {
public:
    FilterNode() : Node("filter_node"), prev_filtered_(0.0) {

        this->declare_parameter("alpha", 0.1);
        alpha_ = this->get_parameter("alpha").as_double();

        sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/sensor/raw", 10,
            std::bind(&FilterNode::callback, this, std::placeholders::_1));

        pub_ = this->create_publisher<std_msgs::msg::Float64>("/sensor/filtered", 10);

        RCLCPP_INFO(this->get_logger(), "Filter node started (alpha=%.2f)", alpha_);
    }

private:
    void callback(const std_msgs::msg::Float64::SharedPtr msg) {
        double raw = msg->data;

        double filtered = alpha_ * raw + (1 - alpha_) * prev_filtered_;
        prev_filtered_ = filtered;

        std_msgs::msg::Float64 out_msg;
        out_msg.data = filtered;
        pub_->publish(out_msg);
    }

    double alpha_;
    double prev_filtered_;

    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr sub_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pub_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FilterNode>());
    rclcpp::shutdown();
    return 0;
}